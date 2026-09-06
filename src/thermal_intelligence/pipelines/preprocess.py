"""Stage 2: Preprocessing.

Validates raw ingested data and applies cleaning/normalization, writing the result
to `data/interim/`.

Usage:
    python -m thermal_intelligence.pipelines.preprocess
"""

from __future__ import annotations

import logging

import pandas as pd

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.data.preprocessing import preprocess
from thermal_intelligence.data.validation import validate_firms_schema

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    raw_dir = settings.data_root / "raw" / "firms"
    raw_files = sorted(raw_dir.glob("*.csv"))
    if not raw_files:
        logger.warning("No raw FIRMS files found in %s — run ingest first.", raw_dir)
        return

    frames = [pd.read_csv(f) for f in raw_files]
    df = pd.concat(frames, ignore_index=True)

    report = validate_firms_schema(df)
    if not report.is_valid:
        logger.warning("Validation found %d issue(s): %s", report.n_errors, report.errors)

    df_clean = preprocess(df)

    interim_dir = settings.data_root / "interim"
    interim_dir.mkdir(parents=True, exist_ok=True)
    out_path = interim_dir / "firms_preprocessed.parquet"
    df_clean.to_parquet(out_path, index=False)
    logger.info("Wrote %d preprocessed rows to %s", len(df_clean), out_path)


if __name__ == "__main__":
    main()
