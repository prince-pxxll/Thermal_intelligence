from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "experiments" / "day4" / "ablations" / "E3_context" / "e3_dataset.parquet"
OUTPUT = ROOT / "experiments" / "day4" / "ablations" / "E3_context" / "e3_scores.parquet"

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


def robust_extremeness(series):
    median = series.median()
    mad = (series - median).abs().median()

    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=series.index)

    return (0.6745 * (series - median) / mad).abs()


def component_score(df, features):
    scores = [robust_extremeness(df[f]) for f in features]
    return pd.concat(scores, axis=1).mean(axis=1)


def proximity_score(distance):
    return 1.0 / (1.0 + distance / 1000.0)


def main():
    df = pd.read_parquet(INPUT)

    df["e3_thermal_score"] = component_score(df, THERMAL_FEATURES)
    df["e3_temporal_score"] = component_score(df, TEMPORAL_FEATURES)
    df["e3_spatial_score"] = component_score(df, SPATIAL_FEATURES)

    industry = proximity_score(df["distance_to_industry_m"])
    road = proximity_score(df["distance_to_road_m"])
    farmland = proximity_score(df["distance_to_farmland_m"])

    df["industry_context_score"] = industry
    df["road_context_score"] = road
    df["farmland_context_score"] = farmland

    df["e3_geospatial_score"] = (
        industry + road + farmland
    ) / 3.0

    df["e3_raw_score"] = (
        0.50 * df["e3_thermal_score"]
        + 0.20 * df["e3_temporal_score"]
        + 0.15 * df["e3_spatial_score"]
        + 0.15 * df["e3_geospatial_score"]
    )

    df["e3_percentile"] = df["e3_raw_score"].rank(pct=True) * 100

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E3 GEOSPATIAL CONTEXT ABLATION")
    print("=" * 60)
    print(f"Events: {len(df)}")
    print("Weights: thermal=0.50, temporal=0.20, spatial=0.15, geo=0.15")
    print()
    print("Score statistics:")
    print(df["e3_raw_score"].describe().to_string())
    print()
    print("Top 5:")
    print(
        df[
            [
                "event_id",
                "e3_thermal_score",
                "e3_temporal_score",
                "e3_spatial_score",
                "e3_geospatial_score",
                "e3_raw_score",
                "e3_percentile",
            ]
        ]
        .sort_values("e3_raw_score", ascending=False)
        .head(5)
        .to_string(index=False)
    )
    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
