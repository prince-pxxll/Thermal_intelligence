from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "experiments" / "day4" / "ablations" / "E2_spatial" / "e2_dataset.parquet"
OUTPUT = ROOT / "experiments" / "day4" / "ablations" / "E2_spatial" / "e2_scores.parquet"

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


def robust_extremeness(series):
    median = series.median()
    mad = (series - median).abs().median()

    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=series.index)

    return (0.6745 * (series - median) / mad).abs()


def component_score(df, features):
    scores = [robust_extremeness(df[feature]) for feature in features]
    return pd.concat(scores, axis=1).mean(axis=1)


def main():
    df = pd.read_parquet(INPUT)

    df["e2_thermal_score"] = component_score(df, THERMAL_FEATURES)
    df["e2_temporal_score"] = component_score(df, TEMPORAL_FEATURES)
    df["e2_spatial_score"] = component_score(df, SPATIAL_FEATURES)

    df["e2_raw_score"] = (
        0.60 * df["e2_thermal_score"]
        + 0.25 * df["e2_temporal_score"]
        + 0.15 * df["e2_spatial_score"]
    )

    df["e2_percentile"] = df["e2_raw_score"].rank(pct=True) * 100

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E2 SPATIAL ABLATION")
    print("=" * 60)
    print(f"Events: {len(df)}")
    print("Weights: thermal=0.60, temporal=0.25, spatial=0.15")
    print()
    print("Score statistics:")
    print(df["e2_raw_score"].describe().to_string())
    print()
    print("Top 5:")
    print(
        df[
            [
                "event_id",
                "e2_thermal_score",
                "e2_temporal_score",
                "e2_spatial_score",
                "e2_raw_score",
                "e2_percentile",
            ]
        ]
        .sort_values("e2_raw_score", ascending=False)
        .head(5)
        .to_string(index=False)
    )
    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
