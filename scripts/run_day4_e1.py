from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "feature_table.parquet"
OUTPUT = (
    ROOT
    / "experiments"
    / "day4"
    / "ablations"
    / "E1_temporal"
    / "e1_dataset.parquet"
)

THERMAL_FEATURES = [
    "mean_frp",
    "median_frp",
    "max_frp",
    "mean_brightness_ti4",
    "max_brightness_ti4",
    "mean_brightness_ti5",
    "confidence_high_ratio",
]

TEMPORAL_FEATURES = [
    "active_days",
    "temporal_span_days",
    "detection_frequency_per_day",
    "night_activity_ratio",
]

def main():
    df = pd.read_parquet(INPUT)

    real = df[~df["event_id"].str.startswith("evt_noise_")].copy()

    result = real[
        ["event_id"] + THERMAL_FEATURES + TEMPORAL_FEATURES
    ].copy()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E1 TEMPORAL ABLATION")
    print("=" * 60)
    print(f"Rows: {len(result)}")
    print(f"Thermal features: {len(THERMAL_FEATURES)}")
    print(f"Temporal features: {len(TEMPORAL_FEATURES)}")
    print(
        f"Missing values: "
        f"{int(result[THERMAL_FEATURES + TEMPORAL_FEATURES].isna().sum().sum())}"
    )
    print(f"Unique events: {result['event_id'].nunique()}")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
