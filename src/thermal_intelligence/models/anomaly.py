"""Unsupervised anomaly detection over thermal event features.

Flags events that deviate from expected seasonal/spatial patterns, independent of
(and complementary to) the supervised classifier in `classification.py`. See
docs/limitations.md — "anomaly is not automatically risk".
"""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

DEFAULT_FEATURES = ["brightness_ti4", "frp", "persistence_score", "hour_of_day"]


def fit_anomaly_detector(
    feature_table: pd.DataFrame,
    features: list[str] = DEFAULT_FEATURES,
    contamination: float = 0.05,
    random_seed: int = 42,
) -> tuple[IsolationForest, StandardScaler]:
    """Fit an Isolation Forest on the given numeric features.

    Returns the fitted `(model, scaler)` pair; scaler is applied before scoring so
    features with different natural scales (e.g. FRP in MW vs. hour_of_day in 0-23)
    don't distort the isolation splits.
    """
    scaler = StandardScaler()
    X = scaler.fit_transform(feature_table[features])
    model = IsolationForest(contamination=contamination, random_state=random_seed)
    model.fit(X)
    return model, scaler


def score_anomalies(
    model: IsolationForest,
    scaler: StandardScaler,
    feature_table: pd.DataFrame,
    features: list[str] = DEFAULT_FEATURES,
) -> pd.Series:
    """Score events for anomalousness; higher = more anomalous.

    `IsolationForest.decision_function` returns higher values for inliers, so we
    negate it to get an intuitive "higher score = more anomalous" convention
    matching `risk_scoring` expectations in config/project.yaml.
    """
    X = scaler.transform(feature_table[features])
    raw_scores = model.decision_function(X)
    return pd.Series(-raw_scores, index=feature_table.index, name="anomaly_score")
