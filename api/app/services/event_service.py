"""Service layer: loads risk-scored event data and applies query filters.

Kept separate from `routes/` so the data-access logic is testable without spinning
up FastAPI, and separate from `thermal_intelligence.risk` since this layer is about
serving already-computed results, not computing them.
"""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from thermal_intelligence.config.settings import get_settings


@lru_cache(maxsize=1)
def _load_events() -> pd.DataFrame:
    settings = get_settings()
    path = settings.results_root / "tables" / "risk_scored_events.parquet"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def get_events(
    min_risk_score: float | None = None,
    district: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> tuple[int, pd.DataFrame]:
    """Return `(total_matching, page)` of risk-scored events matching the filters."""
    df = _load_events()
    if df.empty:
        return 0, df

    if min_risk_score is not None:
        df = df[df["risk_score"] >= min_risk_score]
    if district is not None:
        df = df[df["district"] == district]

    total = len(df)
    page = df.sort_values("risk_score", ascending=False).iloc[offset : offset + limit]
    return total, page


def get_event_by_id(event_id: str) -> pd.Series | None:
    df = _load_events()
    match = df[df["event_id"] == event_id]
    if match.empty:
        return None
    return match.iloc[0]


def reload_events_cache() -> None:
    """Force a refresh of the cached events table (e.g. after a new pipeline run)."""
    _load_events.cache_clear()
