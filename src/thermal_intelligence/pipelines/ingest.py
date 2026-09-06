"""Stage 1: Ingestion.

Pulls raw FIRMS detections (and, where configured, OSM/Sentinel supplementary data)
for the configured region and date range, and writes them unmodified to `data/raw/`.

Usage:
    python -m thermal_intelligence.pipelines.ingest
"""

from __future__ import annotations

import logging
from datetime import date, timedelta

import yaml

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.data.firms import FirmsQuery, fetch_detections, save_raw

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    with open(settings.region_config_path, encoding="utf-8") as f:
        region_cfg = yaml.safe_load(f)["region"]
    bbox = region_cfg["bounding_box"]

    lookback_days = 30  # TODO: read from config/project.yaml ingestion.firms.lookback_days
    end_date = date.today()
    start_date = end_date - timedelta(days=lookback_days)

    query = FirmsQuery(
        min_lat=bbox["min_lat"],
        max_lat=bbox["max_lat"],
        min_lon=bbox["min_lon"],
        max_lon=bbox["max_lon"],
        start_date=start_date,
        end_date=end_date,
    )

    logger.info("Fetching FIRMS detections for %s to %s", start_date, end_date)
    df = fetch_detections(query)
    out_path = save_raw(df, settings.data_root / "raw" / "firms", query)
    logger.info("Saved %d raw detections to %s", len(df), out_path)

    # TODO: also trigger OSM (geospatial.osm) and, if enabled, Sentinel ingestion here.


if __name__ == "__main__":
    main()
