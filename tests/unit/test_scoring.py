"""Unit tests for thermal_intelligence.risk.scoring."""

from __future__ import annotations

import pandas as pd

from thermal_intelligence.risk.scoring import compute_risk_score, context_severity


def _feature_table() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "persistence_score": [0.0, 0.5, 1.0],
            "anomaly_score": [0.0, 0.5, 1.0],
            "classification_confidence": [0.5, 0.5, 0.9],
            "dist_to_industrial_m": [50_000, 2_000, 100],
            "dist_to_forest_m": [50_000, 500, 50],
        }
    )


def test_context_severity_higher_when_closer() -> None:
    table = _feature_table()
    severity = context_severity(table)
    assert severity.iloc[2] > severity.iloc[0]


def test_compute_risk_score_within_bounds() -> None:
    table = _feature_table()
    scores = compute_risk_score(table)
    assert (scores >= 0).all()
    assert (scores <= 100).all()
    # Highest-persistence/anomaly/proximity row should score highest.
    assert scores.iloc[2] == scores.max()
