"""Stage 3: Build joined/derived source datasets.

Clusters preprocessed detections into spatiotemporal events and joins them against
OSM context layers, writing the joined result to `data/processed/`.

Usage:
    python -m thermal_intelligence.pipelines.build_sources
"""

from __future__ import annotations

import logging

import pandas as pd
import yaml

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.geospatial.clustering import assign_event_ids, st_dbscan

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    with open("config/project.yaml", encoding="utf-8") as f:
        project_cfg = yaml.safe_load(f)
    clustering_cfg = project_cfg["clustering"]

    interim_path = settings.data_root / "interim" / "firms_preprocessed.parquet"
    if not interim_path.exists():
        logger.warning("No preprocessed data found at %s — run preprocess first.", interim_path)
        return

    df = pd.read_parquet(interim_path)

    cluster_labels = st_dbscan(
        df,
        spatial_eps_km=clustering_cfg["spatial_eps_km"],
        temporal_eps_hours=clustering_cfg["temporal_eps_hours"],
        min_samples=clustering_cfg["min_samples"],
    )
    df["cluster_id"] = cluster_labels
    df["event_id"] = assign_event_ids(df)

    # TODO: join OSM land-use/industrial/road context here via
    # geospatial.spatial_features once a land-use layer has been fetched and cached
    # under data/raw/osm/ (see geospatial/osm.py).

    processed_dir = settings.data_root / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / "events_with_context.parquet"
    df.to_parquet(out_path, index=False)
    logger.info("Wrote %d clustered/contextualized detections to %s", len(df), out_path)


if __name__ == "__main__":
    main()
