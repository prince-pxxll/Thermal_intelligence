from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "feature_table.parquet"
OUTPUT = ROOT / "experiments" / "day4" / "ablations" / "E0_raw" / "e0_dataset.parquet"

FEATURES = [
    "mean_frp",
    "median_frp",
    "max_frp",
    "mean_brightness_ti4",
    "max_brightness_ti4",
    "mean_brightness_ti5",
    "confidence_high_ratio",
]


def main():
    df = pd.read_parquet(INPUT)

    result = df[["event_id"] + FEATURES].copy()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_parquet(OUTPUT, index=False)

    print("=" * 60)
    print("DAY 4 - E0 RAW THERMAL BASELINE")
    print("=" * 60)
    print(f"Rows: {len(result)}")
    print(f"Features: {len(FEATURES)}")
    print(f"Missing values: {int(result[FEATURES].isna().sum().sum())}")
    print(f"Unique events: {result['event_id'].nunique()}")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
