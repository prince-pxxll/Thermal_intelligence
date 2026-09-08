from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


INPUT = Path("data/processed/events_with_context.parquet")
OUTPUT = Path("data/processed/thermal_sources.parquet")

PROJECTED_CRS = "EPSG:32643"


df = pd.read_parquet(INPUT)
df["acq_datetime_ist"] = pd.to_datetime(df["acq_datetime_ist"])

points = gpd.GeoDataFrame(
    df.copy(),
    geometry=gpd.points_from_xy(
        df["longitude"],
        df["latitude"],
    ),
    crs="EPSG:4326",
).to_crs(PROJECTED_CRS)


def summarize(group: pd.DataFrame) -> pd.Series:
    first_seen = group["acq_datetime_ist"].min()
    last_seen = group["acq_datetime_ist"].max()

    active_days = group["acq_datetime_ist"].dt.date.nunique()

    temporal_span_days = (
        last_seen - first_seen
    ).total_seconds() / 86400

    centroid_x = group.geometry.x.mean()
    centroid_y = group.geometry.y.mean()

    dx = group.geometry.x - centroid_x
    dy = group.geometry.y - centroid_y

    radial_distance_km = np.sqrt(dx**2 + dy**2) / 1000.0

    spatial_std_km = (
        radial_distance_km.std()
        if len(group) > 1
        else np.nan
    )

    return pd.Series(
        {
            "n_observations": len(group),
            "first_seen": first_seen,
            "last_seen": last_seen,
            "active_days": active_days,
            "temporal_span_days": temporal_span_days,

            "detection_frequency_per_day": (
                len(group) / max(active_days, 1)
            ),

            "centroid_lat": group["latitude"].mean(),
            "centroid_lon": group["longitude"].mean(),

            "cluster_radius_km": radial_distance_km.max(),

            "spatial_std_km": spatial_std_km,

            "spatial_observations": len(group),
            "spatial_variation_observable": len(group) > 1,

            "mean_frp": group["frp"].mean(),
            "median_frp": group["frp"].median(),
            "max_frp": group["frp"].max(),
            "frp_std": group["frp"].std(),

            "mean_brightness_ti4": group["bright_ti4"].mean(),
            "max_brightness_ti4": group["bright_ti4"].max(),
            "mean_brightness_ti5": group["bright_ti5"].mean(),

            "night_activity_ratio": (
                group["daynight"] == "N"
            ).mean(),

            "day_activity_ratio": (
                group["daynight"] == "D"
            ).mean(),

            "confidence_high_ratio": (
                group["confidence"] == "high"
            ).mean(),
        }
    )


sources = (
    points.groupby("event_id", sort=True)
    .apply(
        summarize,
        include_groups=False,
    )
    .reset_index()
)


sources["cluster_method"] = "baseline_st_dbscan"
sources["spatial_eps_km"] = 1.0
sources["temporal_eps_hours"] = 48.0
sources["min_samples"] = 2
sources["projected_crs"] = PROJECTED_CRS


OUTPUT.parent.mkdir(parents=True, exist_ok=True)

sources.to_parquet(
    OUTPUT,
    index=False,
)


print("Research-grade source registry created")
print("Sources:", len(sources))
print("Columns:", len(sources.columns))
print()
print(
    sources[
        [
            "event_id",
            "n_observations",
            "active_days",
            "cluster_radius_km",
            "spatial_std_km",
            "spatial_variation_observable",
        ]
    ]
    .head(10)
    .to_string(index=False)
)
print()
print(f"Saved: {OUTPUT}")