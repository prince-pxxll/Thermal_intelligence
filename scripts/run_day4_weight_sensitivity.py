from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "experiments" / "day4" / "ablations" / "E3_context" / "e3_scores.parquet"
OUTPUT = ROOT / "experiments" / "day4" / "robustness" / "weight_sensitivity.csv"

df = pd.read_parquet(INPUT)

baseline = df["e3_percentile"]

variants = {
    "baseline": (0.50, 0.20, 0.15, 0.15),
    "thermal_heavy": (0.60, 0.15, 0.10, 0.15),
    "temporal_heavy": (0.45, 0.30, 0.10, 0.15),
    "spatial_heavy": (0.45, 0.20, 0.20, 0.15),
    "geo_heavy": (0.45, 0.20, 0.10, 0.25),
}

rows = []

for name, weights in variants.items():

    score = (
        weights[0] * df["e3_thermal_score"]
        + weights[1] * df["e3_temporal_score"]
        + weights[2] * df["e3_spatial_score"]
        + weights[3] * df["e3_geospatial_score"]
    )

    rank = score.rank(pct=True) * 100

    rows.append(
        {
            "variant": name,
            "thermal_weight": weights[0],
            "temporal_weight": weights[1],
            "spatial_weight": weights[2],
            "geo_weight": weights[3],
            "spearman_vs_baseline": spearmanr(
                baseline,
                rank
            ).statistic,
        }
    )

result = pd.DataFrame(rows)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("=" * 60)
print("DAY 4 - WEIGHT SENSITIVITY")
print("=" * 60)
print(result.to_string(index=False))
print()
print(f"Saved: {OUTPUT}")
