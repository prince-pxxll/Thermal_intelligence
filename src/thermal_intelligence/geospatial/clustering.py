"""Spatiotemporal clustering of thermal detections into coherent "events".

Groups raw point detections that are close in both space and time into a single
event, so downstream persistence/context/risk features operate on events rather
than raw pixels. See docs/methodology.md, section 3.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

EARTH_RADIUS_KM = 6371.0088


def st_dbscan(
    df: pd.DataFrame,
    spatial_eps_km: float = 1.0,
    temporal_eps_hours: float = 48.0,
    min_samples: int = 2,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    time_col: str = "acq_datetime_ist",
) -> pd.Series:
    """Assign a cluster (event) ID to each detection using a spatiotemporal DBSCAN.

    Approach: scale the temporal axis into spatial-equivalent km using
    `temporal_eps_hours` as the time budget corresponding to `spatial_eps_km`, then
    run a single DBSCAN over the combined (lat, lon, scaled_time) space with
    haversine-consistent scaling.

    Returns a `pd.Series` of cluster labels aligned to `df.index` (-1 = noise/no
    cluster, per scikit-learn DBSCAN convention).

    Note: for larger datasets, consider a proper ST-DBSCAN implementation with a
    haversine metric on lat/lon and a separate temporal threshold, rather than this
    scaled-Euclidean approximation.
    """
    coords_rad = np.radians(df[[lat_col, lon_col]].to_numpy())
    time_hours = (
        df[time_col].astype("int64") / 3_600_000_000_000
    )  # ns -> hours
    time_scaled_km = (time_hours / temporal_eps_hours) * spatial_eps_km

    # Haversine distance needs its own metric; here we approximate by projecting
    # lat/lon to km via a local equirectangular approximation, which is adequate at
    # Maharashtra's latitude range for eps on the order of ~1km. For higher precision,
    # reproject to config.regions.maharashtra.crs.projected before clustering.
    lat0 = coords_rad[:, 0].mean()
    x_km = coords_rad[:, 1] * np.cos(lat0) * EARTH_RADIUS_KM
    y_km = coords_rad[:, 0] * EARTH_RADIUS_KM

    features = np.column_stack([x_km, y_km, time_scaled_km])
    labels = DBSCAN(eps=spatial_eps_km, min_samples=min_samples).fit_predict(features)
    return pd.Series(labels, index=df.index, name="cluster_id")


def assign_event_ids(df: pd.DataFrame, cluster_col: str = "cluster_id") -> pd.Series:
    """Convert integer cluster labels into stable string event IDs.

    Noise points (-1) each get their own singleton event ID rather than being merged.
    """
    labels = df[cluster_col]
    noise_mask = labels == -1
    event_ids = labels.astype(str).radd("evt_")
    if noise_mask.any():
        singleton_ids = [f"evt_noise_{i}" for i in range(noise_mask.sum())]
        event_ids.loc[noise_mask] = singleton_ids
    return event_ids.rename("event_id")
