"""Unit tests for thermal_intelligence.features.persistence."""

from __future__ import annotations

import pandas as pd

from thermal_intelligence.features.persistence import persistence_score


def test_persistence_score_is_bounded_and_monotonic() -> None:
    counts = pd.Series([0, 1, 3, 10, 100])
    scores = persistence_score(counts, min_recurrences_for_flag=3)

    assert (scores >= 0).all()
    assert (scores < 1).all()
    assert scores.is_monotonic_increasing


def test_persistence_score_zero_recurrence_is_zero() -> None:
    counts = pd.Series([0])
    scores = persistence_score(counts)
    assert scores.iloc[0] == 0
