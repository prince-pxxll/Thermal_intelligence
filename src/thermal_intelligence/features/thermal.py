"""Thermal-signature feature extraction from raw FIRMS fields."""

from __future__ import annotations

import pandas as pd


def build_thermal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract the canonical thermal feature set (see config/features/feature_schema.yaml).

    Expects columns: brightness (-> brightness_ti4), bright_t31 (-> brightness_ti5),
    frp, confidence, daynight, satellite.
    """
    out = pd.DataFrame(index=df.index)
    out["brightness_ti4"] = df["brightness"]
    out["brightness_ti5"] = df.get("bright_t31")
    out["frp"] = df["frp"]
    out["confidence"] = df["confidence"]
    out["daynight"] = df["daynight"]
    out["satellite"] = df["satellite"]
    return out
