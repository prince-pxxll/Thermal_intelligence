import pandas as pd
from pathlib import Path

SOURCES = Path("data/processed/thermal_sources.parquet")
ROBUSTNESS = Path("experiments/clustering/source_robustness_summary.csv")
OUTPUT = Path("experiments/clustering/candidate_source_tiers.csv")

sources = pd.read_parquet(SOURCES)
robustness = pd.read_csv(ROBUSTNESS)

df = sources.merge(
    robustness[
        [
            "event_id",
            "mean_jaccard",
            "median_jaccard",
            "min_jaccard",
            "max_jaccard",
            "configs_ge_0_5",
            "configs_ge_0_8",
            "configs_with_match",
            "robustness_class",
        ]
    ],
    on="event_id",
    how="left",
)

def assign_tier(row):
    persistent = row["active_days"] >= 3
    robust = row["robustness_class"] == "high"

    if persistent and robust:
        return "A_persistent_robust"

    if persistent:
        return "B_persistent_sensitive"

    if row["n_observations"] > 1:
        return "C_recurrent_weak"

    return "D_singleton"

df["candidate_tier"] = df.apply(assign_tier, axis=1)

df = df.sort_values(
    ["candidate_tier", "active_days", "n_observations", "median_jaccard"],
    ascending=[True, False, False, False],
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("Candidate source tiers")
print()
print(df[
    [
        "event_id",
        "n_observations",
        "active_days",
        "temporal_span_days",
        "median_jaccard",
        "robustness_class",
        "candidate_tier",
    ]
].to_string(index=False))

print()
print("Tier counts:")
print(df["candidate_tier"].value_counts())

print()
print(f"Saved: {OUTPUT}")
