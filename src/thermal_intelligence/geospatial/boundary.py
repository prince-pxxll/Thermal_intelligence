"""Administrative boundary utilities for spatial filtering."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd


def load_boundary(path: str | Path, target_crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    """Load an administrative boundary and reproject it to the target CRS."""
    boundary = gpd.read_file(path)
    return boundary.to_crs(target_crs)


def filter_points_to_boundary(
    df: pd.DataFrame,
    boundary: gpd.GeoDataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
) -> gpd.GeoDataFrame:
    """Return only observations whose coordinates fall inside the boundary."""
    points = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326",
    )

    boundary_union = boundary.unary_union
    points["inside_boundary"] = points.geometry.within(boundary_union)

    return points.loc[points["inside_boundary"]].reset_index(drop=True)