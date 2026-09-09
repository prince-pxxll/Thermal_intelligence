from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "experiments" / "day4" / "ablations" / "E0_raw" / "e0_dataset.parquet"
OUTPUT = ROOT / "experiments" / "day4" / "ablations" / "E0_raw" / "e0_scores.parquet"

FEATURES = [
    "mean_frp",
    "median_frp",
    "max_frp",
    "mean_brightness_ti4",
    "max_brightness_ti4",
    "mean_brightness_ti5",
]


def robust_extremeness(series):
    x = pd.to_numeric(series, errors="coerce")

    median = x.median()
    mad = (x - median).abs().median()

    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=x.index)

    return (0.6745 * (x - median) / mad).abs()


def main():
    df = pd.read_parquet(INPUT)

    real = df[~df["event_id"].str.startswith("evt_noise_")].copy()

    component_names = []

    for feature in FEATURES:
        name = f"thermal_extreme_{feature}"
        real[name] = robust_extremeness(real[feature])
        component_names.append(name)

    real["e0_raw_score"] = real[component_names].mean(axis=1)

    real["e0_percentile"] = (
        real["e0_raw_score"].rank(pct=True) * 100
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    real.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E0 THERMAL BASELINE")
    print("=" * 60)
    print(f"Evaluation events: {len(real)}")
    print(f"Thermal features: {len(FEATURES)}")
    print(f"Missing values: {int(real[FEATURES].isna().sum().sum())}")
    print()
    print("Score statistics:")
    print(real["e0_raw_score"].describe().to_string())
    print()
    print("Top 5 thermal-extreme events:")
    print(
        real[
            ["event_id", "e0_raw_score", "e0_percentile"]
        ]
        .sort_values("e0_raw_score", ascending=False)
        .head(5)
        .to_string(index=False)
    )
    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
