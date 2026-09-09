from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "experiments" / "day4" / "ablations" / "E1_temporal" / "e1_dataset.parquet"
OUTPUT = ROOT / "experiments" / "day4" / "ablations" / "E1_temporal" / "e1_scores.parquet"

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


def robust_extremeness(series):
    median = series.median()
    mad = (series - median).abs().median()

    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=series.index)

    return (0.6745 * (series - median) / mad).abs()


def main():
    df = pd.read_parquet(INPUT)

    thermal_scores = []
    temporal_scores = []

    for feature in THERMAL_FEATURES:
        thermal_scores.append(robust_extremeness(df[feature]))

    for feature in TEMPORAL_FEATURES:
        temporal_scores.append(robust_extremeness(df[feature]))

    df["e1_thermal_score"] = pd.concat(thermal_scores, axis=1).mean(axis=1)
    df["e1_temporal_score"] = pd.concat(temporal_scores, axis=1).mean(axis=1)

    df["e1_raw_score"] = (
        0.70 * df["e1_thermal_score"]
        + 0.30 * df["e1_temporal_score"]
    )

    df["e1_percentile"] = df["e1_raw_score"].rank(pct=True) * 100

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E1 TEMPORAL ABLATION")
    print("=" * 60)
    print(f"Events: {len(df)}")
    print(f"Thermal weight: 0.70")
    print(f"Temporal weight: 0.30")
    print()
    print("E1 score statistics:")
    print(df["e1_raw_score"].describe().to_string())
    print()
    print("Top 5:")
    print(
        df[["event_id", "e1_thermal_score", "e1_temporal_score",
            "e1_raw_score", "e1_percentile"]]
        .sort_values("e1_raw_score", ascending=False)
        .head(5)
        .to_string(index=False)
    )
    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
