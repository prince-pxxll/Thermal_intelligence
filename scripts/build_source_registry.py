import pandas as pd
from pathlib import Path

INPUT = Path("data/processed/events_with_context.parquet")
OUTPUT = Path("data/processed/thermal_sources.parquet")

df = pd.read_parquet(INPUT)

df["acq_datetime_ist"] = pd.to_datetime(df["acq_datetime_ist"])

def summarize(group: pd.DataFrame) -> pd.Series:
    first_seen = group["acq_datetime_ist"].min()
    last_seen = group["acq_datetime_ist"].max()
    active_days = group["acq_datetime_ist"].dt.date.nunique()
    temporal_span_days = (last_seen - first_seen).total_seconds() / 86400

    lat_center = group["latitude"].mean()
    lon_center = group["longitude"].mean()

    lat_km = (group["latitude"] - lat_center) * 111.32
    lon_km = (
        (group["longitude"] - lon_center)
        * 111.32
        * __import__("numpy").cos(__import__("numpy").radians(lat_center))
    )

    radial_distance_km = (lat_km**2 + lon_km**2) ** 0.5

    return pd.Series(
        {
            "n_observations": len(group),
            "first_seen": first_seen,
            "last_seen": last_seen,
            "active_days": active_days,
            "temporal_span_days": temporal_span_days,
            "detection_frequency_per_day": (
                len(group) / max(temporal_span_days + 1, 1)
            ),
            "centroid_lat": lat_center,
            "centroid_lon": lon_center,
            "cluster_radius_km": radial_distance_km.max(),
            "spatial_std_km": radial_distance_km.std(),
            "mean_frp": group["frp"].mean(),
            "median_frp": group["frp"].median(),
            "max_frp": group["frp"].max(),
            "frp_std": group["frp"].std(),
            "mean_brightness_ti4": group["bright_ti4"].mean(),
            "max_brightness_ti4": group["bright_ti4"].max(),
            "mean_brightness_ti5": group["bright_ti5"].mean(),
            "night_activity_ratio": (group["daynight"] == "N").mean(),
            "day_activity_ratio": (group["daynight"] == "D").mean(),
            "confidence_high_ratio": (group["confidence"] == "high").mean(),
        }
    )

sources = df.groupby("event_id", sort=True).apply(
    summarize,
    include_groups=False,
).reset_index()

sources["cluster_method"] = "baseline_st_dbscan"
sources["spatial_eps_km"] = 1.0
sources["temporal_eps_hours"] = 48.0
sources["min_samples"] = 2

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
sources.to_parquet(OUTPUT, index=False)

print("Source registry created")
print("Sources:", len(sources))
print("Columns:", len(sources.columns))
print()
print(sources.head(10).to_string(index=False))
print()
print(f"Saved: {OUTPUT}")
