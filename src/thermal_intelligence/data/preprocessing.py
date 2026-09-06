"""Cleaning and normalization of validated thermal-anomaly data.

Transforms raw FIRMS pulls (post-validation) into the interim layer: deduplicated,
confidence-filtered, timezone-normalized, and CRS-normalized records ready for
geospatial context joins and feature engineering.
"""

from __future__ import annotations

import pandas as pd

CONFIDENCE_RANK = {"low": 0, "l": 0, "nominal": 1, "n": 1, "high": 2, "h": 2}


def normalize_confidence(df: pd.DataFrame) -> pd.DataFrame:
    """Map FIRMS confidence values (which vary by instrument) onto {low, nominal, high}."""
    df = df.copy()
    canonical = {"l": "low", "n": "nominal", "h": "high"}
    df["confidence"] = (
        df["confidence"].astype(str).str.lower().map(lambda v: canonical.get(v, v))
    )
    return df


def filter_by_confidence(df: pd.DataFrame, min_confidence: str = "nominal") -> pd.DataFrame:
    """Drop detections below `min_confidence` (low < nominal < high)."""
    threshold = CONFIDENCE_RANK[min_confidence.lower()]
    ranks = df["confidence"].str.lower().map(CONFIDENCE_RANK)
    return df.loc[ranks >= threshold].reset_index(drop=True)


def deduplicate_detections(
    df: pd.DataFrame, subset: list[str] | None = None
) -> pd.DataFrame:
    """Drop duplicate detections arising from overlapping satellite passes.

    Default dedup key is (latitude, longitude, acq_date, acq_time, satellite) — exact
    repeats. Near-duplicate detections from adjacent pixels are handled later by
    spatiotemporal clustering, not here.
    """
    subset = subset or ["latitude", "longitude", "acq_date", "acq_time", "satellite"]
    return df.drop_duplicates(subset=subset).reset_index(drop=True)


def to_ist_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Combine `acq_date` + `acq_time` (UTC) into a single tz-aware IST datetime column.

    FIRMS reports `acq_time` as an HHMM integer/string in UTC.
    """
    df = df.copy()
    time_str = df["acq_time"].astype(int).astype(str).str.zfill(4)
    utc_dt = pd.to_datetime(
        df["acq_date"].astype(str) + " " + time_str.str[:2] + ":" + time_str.str[2:],
        utc=True,
    )
    df["acq_datetime_ist"] = utc_dt.dt.tz_convert("Asia/Kolkata")
    return df


def preprocess(df: pd.DataFrame, min_confidence: str = "nominal") -> pd.DataFrame:
    """Run the full preprocessing chain: normalize -> filter -> dedup -> timestamps."""
    df = normalize_confidence(df)
    df = filter_by_confidence(df, min_confidence=min_confidence)
    df = deduplicate_detections(df)
    df = to_ist_datetime(df)
    return df
