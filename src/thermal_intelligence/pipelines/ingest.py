"""Stage 1: Ingestion.

Pulls raw FIRMS detections for the configured region and date range and writes
each API window unmodified to ``data/raw/firms/``.

The FIRMS Area API permits a maximum DAY_RANGE of 5 days per request, so longer
study windows are split into reproducible chunks.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta

import yaml

from thermal_intelligence.config.settings import get_settings, load_project_config
from thermal_intelligence.data.firms import FirmsQuery, fetch_detections, save_raw

logger = logging.getLogger(__name__)

MAX_FIRMS_DAYS_PER_REQUEST = 5


def date_windows(
    start_date: date,
    end_date: date,
    window_days: int = MAX_FIRMS_DAYS_PER_REQUEST,
) -> list[tuple[date, date]]:
    """Split an inclusive date range into valid FIRMS API windows."""
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")

    if not 1 <= window_days <= MAX_FIRMS_DAYS_PER_REQUEST:
        raise ValueError(
            f"window_days must be between 1 and {MAX_FIRMS_DAYS_PER_REQUEST}"
        )

    windows: list[tuple[date, date]] = []
    cursor = start_date

    while cursor <= end_date:
        window_end = min(
            cursor + timedelta(days=window_days - 1),
            end_date,
        )
        windows.append((cursor, window_end))
        cursor = window_end + timedelta(days=1)

    return windows


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    with open(settings.region_config_path, encoding="utf-8") as f:
        region_cfg = yaml.safe_load(f)["region"]

    bbox = region_cfg["bounding_box"]

    # Read the study window from config/project.yaml.
    project_cfg = load_project_config()
    lookback_days = project_cfg["ingestion"]["firms"]["lookback_days"]

    end_date = date.today()
    start_date = end_date - timedelta(days=lookback_days - 1)

    windows = date_windows(start_date, end_date)

    logger.info(
        "FIRMS study window: %s to %s (%d days, %d API windows)",
        start_date,
        end_date,
        lookback_days,
        len(windows),
    )

    raw_dir = settings.data_root / "raw" / "firms"
    total_rows = 0

    for window_start, window_end in windows:
        query = FirmsQuery(
            min_lat=bbox["min_lat"],
            max_lat=bbox["max_lat"],
            min_lon=bbox["min_lon"],
            max_lon=bbox["max_lon"],
            start_date=window_start,
            end_date=window_end,
        )

        logger.info(
            "Fetching FIRMS window: %s to %s",
            window_start,
            window_end,
        )

        df = fetch_detections(query)
        out_path = save_raw(df, raw_dir, query)

        total_rows += len(df)

        logger.info(
            "Saved %d raw detections to %s",
            len(df),
            out_path,
        )

    logger.info(
        "FIRMS ingestion complete: %d total raw detections across %d windows",
        total_rows,
        len(windows),
    )


if __name__ == "__main__":
    main()