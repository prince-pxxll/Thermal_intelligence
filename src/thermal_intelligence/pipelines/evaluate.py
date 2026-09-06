"""Stage 6: Evaluate models and produce the final risk-scored output.

Loads trained models, scores the full feature table (anomaly + classification where
available), computes the final risk score + explanation per event, and writes
metrics/figures/reports to `results/`.

Usage:
    python -m thermal_intelligence.pipelines.evaluate
"""

from __future__ import annotations

import json
import logging
import pickle

import pandas as pd
import yaml

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.models.anomaly import score_anomalies
from thermal_intelligence.models.classification import predict as predict_classifier
from thermal_intelligence.risk.explanation import add_explanations
from thermal_intelligence.risk.scoring import compute_risk_score

logger = logging.getLogger(__name__)


def _min_max_normalize(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return series * 0
    return (series - series.min()) / span


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    with open("config/project.yaml", encoding="utf-8") as f:
        project_cfg = yaml.safe_load(f)
    risk_weights = project_cfg["risk_scoring"]["weights"]

    feature_path = settings.data_root / "processed" / "feature_table.parquet"
    artifacts_dir = settings.models_root / "artifacts"
    if not feature_path.exists() or not (artifacts_dir / "anomaly_model.pkl").exists():
        logger.warning("Missing feature table or trained models — run earlier stages first.")
        return

    feature_table = pd.read_parquet(feature_path)

    with open(artifacts_dir / "anomaly_model.pkl", "rb") as f:
        anomaly_bundle = pickle.load(f)
    raw_anomaly = score_anomalies(anomaly_bundle["model"], anomaly_bundle["scaler"], feature_table)
    feature_table["anomaly_score"] = _min_max_normalize(raw_anomaly)

    classifier_path = artifacts_dir / "classifier.pkl"
    if classifier_path.exists():
        with open(classifier_path, "rb") as f:
            clf_bundle = pickle.load(f)
        preds = predict_classifier(clf_bundle["model"], feature_table, clf_bundle["feature_columns"])
        feature_table = pd.concat([feature_table, preds], axis=1)

    feature_table["risk_score"] = compute_risk_score(feature_table, weights=risk_weights)
    feature_table = add_explanations(feature_table)

    results_root = settings.results_root
    (results_root / "tables").mkdir(parents=True, exist_ok=True)
    (results_root / "metrics").mkdir(parents=True, exist_ok=True)

    out_table_path = results_root / "tables" / "risk_scored_events.parquet"
    feature_table.to_parquet(out_table_path, index=False)
    logger.info("Wrote %d risk-scored events to %s", len(feature_table), out_table_path)

    summary = {
        "n_events": len(feature_table),
        "mean_risk_score": float(feature_table["risk_score"].mean()),
        "n_high_risk": int((feature_table["risk_score"] >= 70).sum()),
    }
    metrics_path = results_root / "metrics" / "summary.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    logger.info("Wrote summary metrics to %s: %s", metrics_path, summary)


if __name__ == "__main__":
    main()
