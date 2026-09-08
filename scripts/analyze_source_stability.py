import pandas as pd
from pathlib import Path

from thermal_intelligence.geospatial.clustering import st_dbscan

INPUT = Path("data/interim/clustering_input.parquet")
EVENTS = Path("data/processed/events_with_context.parquet")
OUTPUT = Path("experiments/clustering/source_stability.csv")

CONFIGS = [
    ("C1", 0.25, 24, 2),
    ("C2", 0.50, 24, 2),
    ("C3", 0.50, 48, 3),
    ("C4", 0.75, 48, 3),
    ("C5", 1.00, 48, 2),
    ("C6", 1.00, 72, 3),
]

df = pd.read_parquet(INPUT)
baseline = pd.read_parquet(EVENTS)

# Baseline event membership is represented by row position/index.
baseline = baseline.reset_index(drop=True)
df = df.reset_index(drop=True)

results = []

reference_config = "C5"
reference_labels = baseline["cluster_id"].to_numpy()

reference_events = sorted(
    x for x in pd.Series(reference_labels).unique() if x != -1
)

for reference_cluster in reference_events:
    reference_members = set(
        baseline.index[baseline["cluster_id"] == reference_cluster]
    )

    for config_name, spatial_eps_km, temporal_eps_hours, min_samples in CONFIGS:
        labels = st_dbscan(
            df,
            spatial_eps_km=spatial_eps_km,
            temporal_eps_hours=temporal_eps_hours,
            min_samples=min_samples,
        )

        candidate_clusters = sorted(
            x for x in pd.Series(labels).unique() if x != -1
        )

        best_cluster = None
        best_jaccard = 0.0
        best_intersection = 0
        best_precision = 0.0
        best_recall = 0.0

        for cluster in candidate_clusters:
            members = set(df.index[labels == cluster])

            intersection = len(reference_members & members)
            union = len(reference_members | members)

            if union == 0:
                continue

            jaccard = intersection / union
            precision = intersection / len(members)
            recall = intersection / len(reference_members)

            if jaccard > best_jaccard:
                best_jaccard = jaccard
                best_cluster = int(cluster)
                best_intersection = intersection
                best_precision = precision
                best_recall = recall

        results.append(
            {
                "reference_event": f"evt_{reference_cluster}",
                "reference_config": reference_config,
                "comparison_config": config_name,
                "best_matching_cluster": best_cluster,
                "reference_size": len(reference_members),
                "overlap_count": best_intersection,
                "jaccard_similarity": round(best_jaccard, 4),
                "precision_of_match": round(best_precision, 4),
                "recall_of_match": round(best_recall, 4),
            }
        )

result = pd.DataFrame(results)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("Source stability analysis complete")
print("Reference events:", len(reference_events))
print("Comparisons:", len(result))
print()
print(result.to_string(index=False))
print()
print(f"Saved: {OUTPUT}")
