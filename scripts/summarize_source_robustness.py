import pandas as pd
from pathlib import Path

INPUT = Path("experiments/clustering/source_stability.csv")
OUTPUT = Path("experiments/clustering/source_robustness_summary.csv")

df = pd.read_csv(INPUT)

# Exclude the self-comparison with the reference configuration.
df = df[df["comparison_config"] != "C5"].copy()

summary = (
    df.groupby("reference_event")
    .agg(
        reference_size=("reference_size", "first"),
        mean_jaccard=("jaccard_similarity", "mean"),
        median_jaccard=("jaccard_similarity", "median"),
        min_jaccard=("jaccard_similarity", "min"),
        max_jaccard=("jaccard_similarity", "max"),
        configs_ge_0_5=("jaccard_similarity", lambda s: int((s >= 0.5).sum())),
        configs_ge_0_8=("jaccard_similarity", lambda s: int((s >= 0.8).sum())),
        configs_with_match=("jaccard_similarity", lambda s: int((s > 0).sum())),
    )
    .reset_index()
    .rename(columns={"reference_event": "event_id"})
)

def classify(row):
    if row["median_jaccard"] >= 0.80:
        return "high"
    if row["median_jaccard"] >= 0.50:
        return "moderate"
    return "low"

summary["robustness_class"] = summary.apply(classify, axis=1)

summary = summary.sort_values(
    ["robustness_class", "median_jaccard", "reference_size"],
    ascending=[True, False, False],
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT, index=False)

print("Source robustness summary")
print()
print(summary.to_string(index=False))
print()
print("Robustness counts:")
print(summary["robustness_class"].value_counts())
print()
print(f"Saved: {OUTPUT}")
