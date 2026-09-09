from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "feature_table.parquet"
OUTPUT = (
    ROOT
    / "experiments"
    / "day4"
    / "ablations"
    / "E3_context"
    / "e3_dataset.parquet"
)

THERMAL_FEATURES = [
    "mean_frp",
    "median_frp",
    "max_frp",
    "mean_brightness_ti4",
    "max_brightness_ti4",
    "mean_brightness_ti5",
]

TEMPORAL_FEATURES = [
    "active_days",
    "temporal_span_days",
    "detection_frequency_per_day",
    "night_activity_ratio",
]

SPATIAL_FEATURES = [
    "cluster_radius_km",
    "spatial_std_km",
    "spatial_observations",
]

GEO_FEATURES = [
    "distance_to_industry_m",
    "distance_to_road_m",
    "distance_to_farmland_m",
]

def main():
    df = pd.read_parquet(INPUT)

    real = df[~df["event_id"].str.startswith("evt_noise_")].copy()

    result = real[
        ["event_id"]
        + THERMAL_FEATURES
        + TEMPORAL_FEATURES
        + SPATIAL_FEATURES
        + GEO_FEATURES
        + [
            "industrial_near_1km",
            "road_near_1km",
            "farmland_near_1km",
        ]
    ].copy()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E3 GEOSPATIAL CONTEXT ABLATION")
    print("=" * 60)
    print(f"Rows: {len(result)}")
    print(f"Thermal features: {len(THERMAL_FEATURES)}")
    print(f"Temporal features: {len(TEMPORAL_FEATURES)}")
    print(f"Spatial features: {len(SPATIAL_FEATURES)}")
    print(f"Geospatial features: {len(GEO_FEATURES)}")
    print(f"Missing values: {int(result.isna().sum().sum())}")
    print(f"Unique events: {result['event_id'].nunique()}")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
