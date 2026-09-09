from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]

paths = {
    "E0": ROOT / "experiments" / "day4" / "ablations" / "E0_raw" / "e0_scores.parquet",
    "E1": ROOT / "experiments" / "day4" / "ablations" / "E1_temporal" / "e1_scores.parquet",
    "E2": ROOT / "experiments" / "day4" / "ablations" / "E2_spatial" / "e2_scores.parquet",
    "E3": ROOT / "experiments" / "day4" / "ablations" / "E3_context" / "e3_scores.parquet",
}

e0 = pd.read_parquet(paths["E0"])[["event_id", "e0_raw_score", "e0_percentile"]]
e1 = pd.read_parquet(paths["E1"])[["event_id", "e1_raw_score", "e1_percentile"]]
e2 = pd.read_parquet(paths["E2"])[["event_id", "e2_raw_score", "e2_percentile"]]
e3 = pd.read_parquet(paths["E3"])[["event_id", "e3_raw_score", "e3_percentile"]]

df = (
    e0
    .merge(e1, on="event_id")
    .merge(e2, on="event_id")
    .merge(e3, on="event_id")
)

summary = pd.DataFrame(
    {
        "experiment": ["E0", "E1", "E2", "E3"],
        "mean_score": [
            df["e0_raw_score"].mean(),
            df["e1_raw_score"].mean(),
            df["e2_raw_score"].mean(),
            df["e3_raw_score"].mean(),
        ],
        "median_score": [
            df["e0_raw_score"].median(),
            df["e1_raw_score"].median(),
            df["e2_raw_score"].median(),
            df["e3_raw_score"].median(),
        ],
        "max_score": [
            df["e0_raw_score"].max(),
            df["e1_raw_score"].max(),
            df["e2_raw_score"].max(),
            df["e3_raw_score"].max(),
        ],
    }
)

correlations = pd.DataFrame(
    {
        "comparison": ["E0_E1", "E1_E2", "E2_E3", "E0_E3"],
        "spearman_rank_correlation": [
            spearmanr(df["e0_percentile"], df["e1_percentile"]).statistic,
            spearmanr(df["e1_percentile"], df["e2_percentile"]).statistic,
            spearmanr(df["e2_percentile"], df["e3_percentile"]).statistic,
            spearmanr(df["e0_percentile"], df["e3_percentile"]).statistic,
        ],
    }
)

OUT = ROOT / "experiments" / "day4" / "ablation_comparison"
OUT.mkdir(parents=True, exist_ok=True)

df.to_parquet(OUT / "source_rankings.parquet", index=False)
summary.to_csv(OUT / "score_summary.csv", index=False)
correlations.to_csv(OUT / "rank_correlations.csv", index=False)

print("=" * 60)
print("DAY 4 - FINAL ABLATION SUMMARY")
print("=" * 60)
print()
print(summary.to_string(index=False))
print()
print(correlations.to_string(index=False))
print()
print(f"Saved: {OUT}")
