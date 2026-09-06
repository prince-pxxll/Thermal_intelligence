"""Assembly of the unified per-event feature vector.

Combines thermal, temporal, persistence, and geospatial-context features into the
single model-ready table defined by config/features/feature_schema.yaml.
"""

from __future__ import annotations

import pandas as pd

from thermal_intelligence.features.temporal import build_temporal_features
from thermal_intelligence.features.thermal import build_thermal_features


def assemble_feature_table(
    detections: pd.DataFrame,
    event_ids: pd.Series,
    spatial_context: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Join thermal, temporal, and (optional) spatial-context features into one table.

    `spatial_context` is expected to be indexed by `event_id` and contain columns
    such as `dist_to_industrial_m`, `landuse_category`, `district`, produced by
    `geospatial.spatial_features`. Persistence features are computed separately
    (they require geometry) via `features.persistence` and merged in by the caller
    of this function within `pipelines/build_features.py`.
    """
    thermal = build_thermal_features(detections)
    temporal = build_temporal_features(detections)

    table = pd.concat([event_ids, thermal, temporal], axis=1)

    if spatial_context is not None:
        table = table.merge(spatial_context, on="event_id", how="left")

    return table
