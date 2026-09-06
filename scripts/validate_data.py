#!/usr/bin/env python3
"""CLI wrapper for validating raw or interim data files.

Usage:
    python scripts/validate_data.py data/raw/firms/firms_VIIRS_SNPP_NRT_2026-08-01_2026-08-31.csv
    python scripts/validate_data.py --all-raw
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.data.validation import validate_firms_schema

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=str, help="Path to a specific CSV file to validate")
    parser.add_argument(
        "--all-raw", action="store_true", help="Validate every CSV under data/raw/firms/"
    )
    return parser.parse_args()


def validate_file(path: Path) -> bool:
    df = pd.read_csv(path)
    report = validate_firms_schema(df)
    if report.is_valid:
        logger.info("%s: OK (%d rows)", path, report.n_rows)
    else:
        logger.warning("%s: %d issue(s): %s", path, report.n_errors, report.errors)
    return report.is_valid


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    settings = get_settings()

    if args.all_raw:
        files = sorted((settings.data_root / "raw" / "firms").glob("*.csv"))
        if not files:
            logger.warning("No raw FIRMS files found.")
            sys.exit(1)
        results = [validate_file(f) for f in files]
        sys.exit(0 if all(results) else 1)

    if not args.path:
        logger.error("Provide a file path or use --all-raw")
        sys.exit(2)

    ok = validate_file(Path(args.path))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
