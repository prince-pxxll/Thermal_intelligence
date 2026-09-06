"""Stage 5: Train models.

Trains the event-type classifier (where labels exist) and fits the anomaly detector
on the full feature table, writing both to `models/artifacts/`.

Usage:
    python -m thermal_intelligence.pipelines.train
"""

from __future__ import annotations

import logging
import pickle

import pandas as pd
import yaml

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.models.anomaly import fit_anomaly_detector
from thermal_intelligence.models.classification import train as train_classifier

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    with open("config/project.yaml", encoding="utf-8") as f:
        project_cfg = yaml.safe_load(f)
    modeling_cfg = project_cfg["modeling"]

    feature_path = settings.data_root / "processed" / "feature_table.parquet"
    if not feature_path.exists():
        logger.warning("No feature table found at %s — run build_features first.", feature_path)
        return

    feature_table = pd.read_parquet(feature_path)
    artifacts_dir = settings.models_root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # --- Anomaly detector (unsupervised, always trainable) ---
    anomaly_model, anomaly_scaler = fit_anomaly_detector(
        feature_table, contamination=modeling_cfg["anomaly_detection"]["contamination"]
    )
    with open(artifacts_dir / "anomaly_model.pkl", "wb") as f:
        pickle.dump({"model": anomaly_model, "scaler": anomaly_scaler}, f)
    logger.info("Saved anomaly detector to %s", artifacts_dir / "anomaly_model.pkl")

    # --- Classifier (requires labels; skip gracefully if unavailable) ---
    labels_path = settings.data_root / "labels" / "event_labels.parquet"
    if labels_path.exists():
        labels = pd.read_parquet(labels_path)
        labeled = feature_table.merge(labels, on="event_id", how="inner")
        result = train_classifier(labeled, test_size=modeling_cfg["classification"]["test_size"])
        with open(artifacts_dir / "classifier.pkl", "wb") as f:
            pickle.dump({"model": result.model, "feature_columns": result.feature_columns}, f)
        logger.info("Trained classifier — test accuracy: %.3f", result.test_accuracy)
    else:
        logger.warning(
            "No labels found at %s — skipping classifier training. "
            "Risk scoring will fall back to a neutral classification_confidence.",
            labels_path,
        )


if __name__ == "__main__":
    main()
