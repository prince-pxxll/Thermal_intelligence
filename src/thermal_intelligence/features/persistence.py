"""Persistence scoring: distinguishing one-off from recurring thermal sources.

A thermal source that keeps recurring at roughly the same location over weeks is a
qualitatively different signal than a single-day detection. See
docs/methodology.md, section 4, and docs/assumptions.md for the fixed-radius
buffer assumption this relies on.
"""

from __future__ import annotations

import geopandas as gpd
import pandas as pd


def recurrence_count(
    events: gpd.GeoDataFrame,
    buffer_radius_m: float = 500,
    window_days: int = 30,
    projected_crs: str = "EPSG:32643",
    datetime_col: str = "acq_datetime_ist",
) -> pd.Series:
    """Count how many other events fall within `buffer_radius_m` and `window_days`
    of each event, i.e. a rolling spatial-temporal recurrence count.

    This is intentionally simple (buffer + time window) rather than a full
    space-time kernel density estimate, per the documented persistence assumption.
    """
    proj = events.to_crs(projected_crs)
    buffered = proj.copy()
    buffered["geometry"] = proj.geometry.buffer(buffer_radius_m)

    joined = gpd.sjoin(proj, buffered, how="left", predicate="within", lsuffix="pt", rsuffix="buf")

    time_left = joined[f"{datetime_col}_pt"] if f"{datetime_col}_pt" in joined else joined[datetime_col]
    time_right = joined[f"{datetime_col}_buf"] if f"{datetime_col}_buf" in joined else joined[datetime_col]
    within_window = (time_left - time_right).abs() <= pd.Timedelta(days=window_days)

    counts = joined[within_window].groupby(joined.index)["index_buf"].count()
    return counts.reindex(events.index, fill_value=0).rename("recurrence_count_30d")


def persistence_score(recurrence_counts: pd.Series, min_recurrences_for_flag: int = 3) -> pd.Series:
    """Normalize raw recurrence counts to a bounded [0, 1] persistence score.

    Uses a saturating transform so that very high recurrence counts don't dominate
    the risk-scoring weighted sum disproportionately (see risk/scoring.py).
    """
    normalized = recurrence_counts / (recurrence_counts + min_recurrences_for_flag)
    return normalized.rename("persistence_score")
