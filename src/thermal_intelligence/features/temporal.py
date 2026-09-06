"""Temporal feature extraction: time-of-day, seasonality, detection frequency."""

from __future__ import annotations

import pandas as pd


def _season_flag(dt: pd.Timestamp, region_seasons: dict) -> str:
    month = dt.month
    for name, window in region_seasons.items():
        start, end = window["start_month"], window["end_month"]
        if start <= month <= end:
            return name
    return "other"


def build_temporal_features(
    df: pd.DataFrame, datetime_col: str = "acq_datetime_ist"
) -> pd.DataFrame:
    """Extract hour-of-day, day-of-year, and seasonal-context flags.

    Seasonal windows are read from `config/regions/maharashtra.yaml` ->
    `seasonal_context` so they stay configurable rather than hardcoded.
    """
    import yaml

    from thermal_intelligence.config.settings import get_settings

    settings = get_settings()
    with open(settings.region_config_path, encoding="utf-8") as f:
        region_cfg = yaml.safe_load(f)
    seasons = region_cfg["region"]["seasonal_context"]

    out = pd.DataFrame(index=df.index)
    out["acq_datetime_ist"] = df[datetime_col]
    out["hour_of_day"] = df[datetime_col].dt.hour
    out["day_of_year"] = df[datetime_col].dt.dayofyear
    out["season_flag"] = df[datetime_col].apply(lambda dt: _season_flag(dt, seasons))
    return out
