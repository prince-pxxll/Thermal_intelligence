"""Combine model outputs into a single explainable 0-100 risk score.

Weights are read from config/project.yaml -> risk_scoring.weights so scoring
behavior is tunable without a code change. See docs/methodology.md, section 6.
"""

from __future__ import annotations

import pandas as pd

DEFAULT_WEIGHTS = {
    "persistence": 0.30,
    "anomaly": 0.30,
    "context_severity": 0.25,
    "classification_confidence": 0.15,
}


def context_severity(feature_table: pd.DataFrame) -> pd.Series:
    """Derive a [0, 1] contextual severity score from proximity to sensitive features.

    Closer to industrial zones / forest reserves increases severity; this is a
    simple inverse-distance heuristic, not a learned model — revisit once labeled
    outcome data justifies a data-driven weighting (see docs/decisions/ for any ADR
    superseding this).
    """
    industrial_proximity = 1 / (1 + feature_table.get("dist_to_industrial_m", pd.Series(float("inf"), index=feature_table.index)) / 1000)
    forest_proximity = 1 / (1 + feature_table.get("dist_to_forest_m", pd.Series(float("inf"), index=feature_table.index)) / 1000)
    return ((industrial_proximity + forest_proximity) / 2).rename("context_severity")


def compute_risk_score(
    feature_table: pd.DataFrame,
    weights: dict[str, float] = DEFAULT_WEIGHTS,
    scale_max: float = 100.0,
) -> pd.Series:
    """Weighted combination of persistence, anomaly, context, and classification
    confidence into a single 0-`scale_max` risk score per event.

    All component scores are expected to already be normalized to [0, 1]:
      - persistence_score        (features/persistence.py)
      - anomaly_score            (models/anomaly.py — min-max normalize before calling this)
      - context_severity         (this module)
      - classification_confidence (models/classification.py, already in [0, 1])
    """
    components = pd.DataFrame(
        {
            "persistence": feature_table["persistence_score"],
            "anomaly": feature_table["anomaly_score"],
            "context_severity": context_severity(feature_table),
            "classification_confidence": feature_table.get(
                "classification_confidence", pd.Series(0.5, index=feature_table.index)
            ),
        }
    )
    weighted_sum = sum(components[col] * w for col, w in weights.items())
    return (weighted_sum * scale_max).rename("risk_score")
