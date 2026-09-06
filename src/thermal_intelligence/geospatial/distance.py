"""Distance calculations between thermal events and contextual geographic features."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def nearest_distance_m(
    points: gpd.GeoDataFrame, targets: gpd.GeoDataFrame, projected_crs: str = "EPSG:32643"
) -> pd.Series:
    """Distance in meters from each point in `points` to the nearest geometry in `targets`.

    Both inputs are reprojected to `projected_crs` (default: UTM 43N, appropriate for
    Maharashtra) before computing distances, since geographic-CRS distances are not
    metrically meaningful.
    """
    points_proj = points.to_crs(projected_crs)
    targets_proj = targets.to_crs(projected_crs)

    joined = gpd.sjoin_nearest(
        points_proj, targets_proj, how="left", distance_col="_dist_m"
    )
    # sjoin_nearest can produce duplicate matches on ties; keep the closest per point.
    joined = joined.sort_values("_dist_m").drop_duplicates(subset=points_proj.index.name or "index")
    return joined["_dist_m"].reindex(points.index).rename("distance_m")


def points_from_lat_lon(
    df: pd.DataFrame, lat_col: str = "latitude", lon_col: str = "longitude", crs: str = "EPSG:4326"
) -> gpd.GeoDataFrame:
    """Build a `GeoDataFrame` of Points from lat/lon columns."""
    geometry = [Point(lon, lat) for lat, lon in zip(df[lat_col], df[lon_col], strict=True)]
    return gpd.GeoDataFrame(df.copy(), geometry=geometry, crs=crs)
