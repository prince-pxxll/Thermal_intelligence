from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "thermal_sources.parquet"
OUTPUT = ROOT / "data" / "processed" / "feature_table.parquet"


THERMAL_FEATURES = [
    "mean_frp",
    "median_frp",
    "max_frp",
    "frp_std",
    "mean_brightness_ti4",
    "max_brightness_ti4",
    "mean_brightness_ti5",
    "confidence_high_ratio",
]

TEMPORAL_FEATURES = [
    "first_seen",
    "last_seen",
    "active_days",
    "temporal_span_days",
    "detection_frequency_per_day",
    "night_activity_ratio",
    "day_activity_ratio",
]

SPATIAL_FEATURES = [
    "centroid_lat",
    "centroid_lon",
    "cluster_radius_km",
    "spatial_std_km",
    "spatial_observations",
    "spatial_variation_observable",
]


def main():
    df = pd.read_parquet(INPUT)

    required = (
        ["event_id"]
        + THERMAL_FEATURES
        + TEMPORAL_FEATURES
        + SPATIAL_FEATURES
    )

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required source-level features: {missing}"
        )

    feature_table = df[required].copy()

    feature_table["feature_version"] = "day3_v1_TTS"
    feature_table["context_status"] = "not_available"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    feature_table.to_parquet(OUTPUT, index=False)

    print("Day 3 feature table created")
    print("Rows:", len(feature_table))
    print("Columns:", len(feature_table.columns))
    print()
    print("Feature columns:")
    for column in required:
        print(" -", column)

    print()
    print("Missing values:")
    print(feature_table.isna().sum().to_string())

    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()