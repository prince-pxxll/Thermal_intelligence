"""Unit tests for thermal_intelligence.data.preprocessing."""

from __future__ import annotations

import pandas as pd

from thermal_intelligence.data.preprocessing import (
    deduplicate_detections,
    filter_by_confidence,
    normalize_confidence,
    to_ist_datetime,
)


def test_normalize_confidence_maps_shorthand(sample_firms_df: pd.DataFrame) -> None:
    df = sample_firms_df.copy()
    df.loc[0, "confidence"] = "n"
    out = normalize_confidence(df)
    assert out.loc[0, "confidence"] == "nominal"


def test_filter_by_confidence_drops_low(sample_firms_df: pd.DataFrame) -> None:
    df = normalize_confidence(sample_firms_df)
    out = filter_by_confidence(df, min_confidence="nominal")
    assert "low" not in out["confidence"].str.lower().values


def test_deduplicate_detections_removes_exact_repeats(sample_firms_df: pd.DataFrame) -> None:
    dup_df = pd.concat([sample_firms_df, sample_firms_df.iloc[[0]]], ignore_index=True)
    out = deduplicate_detections(dup_df)
    assert len(out) == len(sample_firms_df)


def test_to_ist_datetime_produces_tz_aware_column(sample_firms_df: pd.DataFrame) -> None:
    out = to_ist_datetime(sample_firms_df)
    assert "acq_datetime_ist" in out.columns
    assert str(out["acq_datetime_ist"].dt.tz) == "Asia/Kolkata"
