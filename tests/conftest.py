"""Shared pytest fixtures for unit and integration tests."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import pytest


@pytest.fixture
def sample_firms_df() -> pd.DataFrame:
    """A small, valid-shaped FIRMS-like DataFrame for unit tests."""
    return pd.DataFrame(
        {
            "latitude": [19.076, 19.077, 18.520, 21.145],
            "longitude": [72.877, 72.878, 73.856, 79.088],
            "brightness": [310.2, 308.9, 295.4, 330.1],
            "scan": [0.4, 0.4, 0.5, 0.6],
            "track": [0.4, 0.4, 0.5, 0.6],
            "acq_date": ["2026-03-01", "2026-03-01", "2026-03-02", "2026-03-05"],
            "acq_time": [530, 545, 1210, 30],
            "satellite": ["N", "N", "1", "N"],
            "confidence": ["nominal", "high", "low", "nominal"],
            "version": ["2.0NRT"] * 4,
            "bright_t31": [290.1, 289.5, 285.0, 295.0],
            "frp": [12.3, 9.8, 3.1, 45.6],
            "daynight": ["D", "D", "D", "N"],
        }
    )


@pytest.fixture
def fixed_now() -> datetime:
    return datetime(2026, 9, 6, 12, 0, 0)
