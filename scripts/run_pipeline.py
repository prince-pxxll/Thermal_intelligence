#!/usr/bin/env python3
"""CLI wrapper to run the full pipeline end-to-end, or a chosen subset of stages.

Equivalent to `make pipeline`, but with the ability to select a subset of stages
and to keep running on a stage failure instead of stopping (useful when iterating).

Usage:
    python scripts/run_pipeline.py
    python scripts/run_pipeline.py --stages ingest preprocess
    python scripts/run_pipeline.py --continue-on-error
"""

from __future__ import annotations

import argparse
import logging

from thermal_intelligence.pipelines import (
    build_features,
    build_sources,
    evaluate,
    ingest,
    preprocess,
    train,
)

logger = logging.getLogger(__name__)

STAGES = {
    "ingest": ingest.main,
    "preprocess": preprocess.main,
    "build_sources": build_sources.main,
    "build_features": build_features.main,
    "train": train.main,
    "evaluate": evaluate.main,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stages",
        nargs="+",
        choices=list(STAGES.keys()),
        default=list(STAGES.keys()),
        help="Which pipeline stages to run, in order (default: all)",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Keep running subsequent stages even if one fails",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    for stage_name in args.stages:
        logger.info("=== Running stage: %s ===", stage_name)
        try:
            STAGES[stage_name]()
        except Exception:
            logger.exception("Stage '%s' failed", stage_name)
            if not args.continue_on_error:
                raise
    logger.info("Pipeline run complete.")


if __name__ == "__main__":
    main()
