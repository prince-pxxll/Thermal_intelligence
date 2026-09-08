"""Thermal-signature feature extraction from FIRMS observations."""

from __future__ import annotations

import pandas as pd


CONFIDENCE_TO_NUMERIC = {
    "low": 0,
    "nominal": 1,
    "high": 2,
}


def build_thermal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build canonical thermal features from the preprocessed FIRMS schema."""

    required = [
        "bright_ti4",
        "bright_ti5",
        "frp",
        "confidence",
        "daynight",
        "satellite",
    ]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required FIRMS thermal columns: {missing}"
        )

    out = pd.DataFrame(index=df.index)

    out["brightness_ti4"] = pd.to_numeric(
        df["bright_ti4"], errors="coerce"
    )

    out["brightness_ti5"] = pd.to_numeric(
        df["bright_ti5"], errors="coerce"
    )

    out["frp"] = pd.to_numeric(
        df["frp"], errors="coerce"
    )

    out["confidence"] = (
        df["confidence"]
        .astype("string")
        .str.lower()
    )

    out["confidence_numeric"] = (
        out["confidence"]
        .map(CONFIDENCE_TO_NUMERIC)
        .astype("Float64")
    )

    out["daynight"] = (
        df["daynight"]
        .astype("string")
        .str.upper()
    )

    out["satellite"] = df["satellite"].astype("string")

    return out