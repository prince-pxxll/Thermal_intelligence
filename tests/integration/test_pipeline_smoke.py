"""Integration smoke test for the ingest -> preprocess -> features chain.

This does not hit any live API. It exercises the preprocessing + feature-assembly
logic together on an in-memory sample dataset to catch integration breaks between
modules that unit tests (which mock/isolate a single module) would miss.
"""

from __future__ import annotations

import pandas as pd

from thermal_intelligence.data.preprocessing import preprocess
from thermal_intelligence.data.validation import validate_firms_schema


def test_preprocess_chain_end_to_end(sample_firms_df: pd.DataFrame) -> None:
    report = validate_firms_schema(sample_firms_df)
    assert report.is_valid

    cleaned = preprocess(sample_firms_df, min_confidence="nominal")

    # low-confidence row should have been dropped
    assert "low" not in cleaned["confidence"].str.lower().values
    # timestamps should be tz-aware IST
    assert str(cleaned["acq_datetime_ist"].dt.tz) == "Asia/Kolkata"
    # no duplicate rows introduced
    assert len(cleaned) <= len(sample_firms_df)
