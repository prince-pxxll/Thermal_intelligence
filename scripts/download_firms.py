#!/usr/bin/env python3
"""CLI wrapper for downloading raw FIRMS detections.

Thin script around `thermal_intelligence.pipelines.ingest` for ad hoc/manual runs
outside the Makefile (e.g. a custom date range instead of the default lookback).

Usage:
    python scripts/download_firms.py --days 14
    python scripts/download_firms.py --start 2026-08-01 --end 2026-08-31
"""

from __future__ import annotations

import argparse
import logging
from datetime import date, timedelta

import yaml

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.data.firms import FirmsQuery, fetch_detections, save_raw

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=None, help="Lookback window in days from today")
    parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--instrument",
        type=str,
        default="VIIRS_SNPP_NRT",
        help="FIRMS instrument, e.g. VIIRS_SNPP_NRT, MODIS_NRT",
    )
    return parser.parse_args()


def resolve_date_range(args: argparse.Namespace) -> tuple[date, date]:
    if args.start and args.end:
        return date.fromisoformat(args.start), date.fromisoformat(args.end)
    days = args.days or 30
    end = date.today()
    return end - timedelta(days=days), end


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    start_date, end_date = resolve_date_range(args)

    settings = get_settings()
    with open(settings.region_config_path, encoding="utf-8") as f:
        bbox = yaml.safe_load(f)["region"]["bounding_box"]

    query = FirmsQuery(
        min_lat=bbox["min_lat"],
        max_lat=bbox["max_lat"],
        min_lon=bbox["min_lon"],
        max_lon=bbox["max_lon"],
        start_date=start_date,
        end_date=end_date,
        instrument=args.instrument,
    )

    logger.info("Downloading FIRMS detections (%s) for %s to %s", args.instrument, start_date, end_date)
    df = fetch_detections(query)
    out_path = save_raw(df, settings.data_root / "raw" / "firms", query)
    logger.info("Saved %d detections to %s", len(df), out_path)


if __name__ == "__main__":
    main()
