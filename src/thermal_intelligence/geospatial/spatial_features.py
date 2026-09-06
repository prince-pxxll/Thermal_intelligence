"""Derived spatial features built from clustering + OSM context.

Combines outputs of `clustering.py`, `distance.py`, and `osm.py` into per-event
spatial feature columns consumed by `features/context.py`.
"""

from __future__ import annotations

import geopandas as gpd
import pandas as pd


def cluster_density(df: pd.DataFrame, event_id_col: str = "event_id") -> pd.Series:
    """Number of raw detections composing each clustered event.

    A higher count for the same event can indicate a larger or longer-burning source.
    """
    counts = df.groupby(event_id_col)[event_id_col].transform("count")
    return counts.rename("cluster_detection_count")


def landuse_at_centroid(
    event_centroids: gpd.GeoDataFrame, landuse_layer: gpd.GeoDataFrame, category_col: str = "landuse"
) -> pd.Series:
    """Spatial-join each event centroid to the land-use polygon it falls within.

    Events falling outside all mapped polygons (common in under-mapped rural areas —
    see docs/limitations.md) receive a null category rather than a guessed default.
    """
    joined = gpd.sjoin(event_centroids, landuse_layer[[category_col, "geometry"]], how="left", predicate="within")
    return joined[category_col].reindex(event_centroids.index).rename("landuse_category")


def event_centroids(df: pd.DataFrame, event_id_col: str = "event_id") -> gpd.GeoDataFrame:
    """Compute the centroid point of each clustered event's constituent detections."""
    from thermal_intelligence.geospatial.distance import points_from_lat_lon

    points = points_from_lat_lon(df)
    centroids = points.dissolve(by=event_id_col).centroid
    return gpd.GeoDataFrame({"event_id": centroids.index}, geometry=centroids.values, crs=points.crs)
