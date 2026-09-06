"""Unit tests for thermal_intelligence.data.validation."""

from __future__ import annotations

import pandas as pd

from thermal_intelligence.data.validation import validate_firms_schema


def test_valid_dataframe_passes(sample_firms_df: pd.DataFrame) -> None:
    report = validate_firms_schema(sample_firms_df)
    assert report.is_valid
    assert report.n_errors == 0
    assert report.n_rows == len(sample_firms_df)


def test_out_of_range_latitude_flagged(sample_firms_df: pd.DataFrame) -> None:
    bad_df = sample_firms_df.copy()
    bad_df.loc[0, "latitude"] = 999.0
    report = validate_firms_schema(bad_df)
    assert not report.is_valid
    assert any("latitude" in e for e in report.errors)


def test_unexpected_confidence_value_flagged(sample_firms_df: pd.DataFrame) -> None:
    bad_df = sample_firms_df.copy()
    bad_df.loc[0, "confidence"] = "extremely_confident"
    report = validate_firms_schema(bad_df)
    assert not report.is_valid
    assert any("confidence" in e for e in report.errors)
