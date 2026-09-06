"""Stage 4: Build the model-ready feature table.

Assembles thermal, temporal, persistence, and context features per
config/features/feature_schema.yaml, writing the result to `data/processed/`.

Usage:
    python -m thermal_intelligence.pipelines.build_features
"""

from __future__ import annotations

import logging

import pandas as pd

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.features.context import assemble_feature_table
from thermal_intelligence.features.persistence import persistence_score, recurrence_count
from thermal_intelligence.geospatial.distance import points_from_lat_lon

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    processed_path = settings.data_root / "processed" / "events_with_context.parquet"
    if not processed_path.exists():
        logger.warning("No processed events found at %s — run build_sources first.", processed_path)
        return

    df = pd.read_parquet(processed_path)
    event_ids = df["event_id"]

    feature_table = assemble_feature_table(df, event_ids)

    points = points_from_lat_lon(df)
    counts = recurrence_count(points)
    feature_table["recurrence_count_30d"] = counts.values
    feature_table["persistence_score"] = persistence_score(counts).values

    out_path = settings.data_root / "processed" / "feature_table.parquet"
    feature_table.to_parquet(out_path, index=False)
    logger.info("Wrote feature table with %d rows to %s", len(feature_table), out_path)


if __name__ == "__main__":
    main()
