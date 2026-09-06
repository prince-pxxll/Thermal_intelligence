"""Event-type classification (agricultural / industrial / wildfire / other).

See docs/methodology.md section 5 and docs/limitations.md for the caveat on label
scarcity affecting generalization.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL_FEATURES = ["confidence", "daynight", "satellite", "season_flag", "landuse_category"]
NUMERIC_FEATURES = [
    "brightness_ti4",
    "frp",
    "hour_of_day",
    "persistence_score",
    "dist_to_industrial_m",
    "dist_to_cropland_m",
    "dist_to_forest_m",
]
TARGET_COLUMN = "event_type"


@dataclass
class TrainResult:
    model: Pipeline
    test_accuracy: float
    feature_columns: list[str]


def build_pipeline(random_seed: int = 42) -> Pipeline:
    """Construct the preprocessing + classifier pipeline.

    Uses a `ColumnTransformer` so categorical and numeric features are handled
    consistently between training and inference.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ],
        remainder="passthrough",
    )
    classifier = GradientBoostingClassifier(random_state=random_seed)
    return Pipeline(steps=[("preprocess", preprocessor), ("classify", classifier)])


def train(
    feature_table: pd.DataFrame, test_size: float = 0.2, random_seed: int = 42
) -> TrainResult:
    """Train the event-type classifier on a labeled feature table.

    `feature_table` must contain `TARGET_COLUMN` (from `data/labels/`) plus the
    feature columns listed in `CATEGORICAL_FEATURES` / `NUMERIC_FEATURES`.
    """
    feature_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES
    X = feature_table[feature_columns]
    y = feature_table[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )

    pipeline = build_pipeline(random_seed=random_seed)
    pipeline.fit(X_train, y_train)
    test_accuracy = pipeline.score(X_test, y_test)

    return TrainResult(model=pipeline, test_accuracy=test_accuracy, feature_columns=feature_columns)


def predict(model: Pipeline, feature_table: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """Predict event type + confidence for new (unlabeled) events."""
    X = feature_table[feature_columns]
    predictions = model.predict(X)
    probabilities = model.predict_proba(X).max(axis=1)
    return pd.DataFrame(
        {
            "predicted_event_type": predictions,
            "classification_confidence": probabilities,
        },
        index=feature_table.index,
    )
