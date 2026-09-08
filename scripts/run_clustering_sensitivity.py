import pandas as pd
from pathlib import Path

from thermal_intelligence.geospatial.clustering import st_dbscan

INPUT = Path("data/interim/clustering_input.parquet")
OUTPUT = Path("experiments/clustering/clustering_sensitivity.csv")

CONFIGS = [
    (0.25, 24, 2),
    (0.50, 24, 2),
    (0.50, 48, 3),
    (0.75, 48, 3),
    (1.00, 48, 2),
    (1.00, 72, 3),
]

df = pd.read_parquet(INPUT)

rows = []

for spatial_eps_km, temporal_eps_hours, min_samples in CONFIGS:
    labels = st_dbscan(
        df,
        spatial_eps_km=spatial_eps_km,
        temporal_eps_hours=temporal_eps_hours,
        min_samples=min_samples,
    )

    clustered = labels[labels != -1]

    rows.append(
        {
            "spatial_eps_km": spatial_eps_km,
            "temporal_eps_hours": temporal_eps_hours,
            "min_samples": min_samples,
            "n_observations": len(labels),
            "n_clusters": clustered.nunique(),
            "n_noise": int((labels == -1).sum()),
            "noise_fraction": round((labels == -1).mean(), 4),
            "largest_cluster": (
                int(clustered.value_counts().max())
                if not clustered.empty
                else 0
            ),
            "median_cluster_size": (
                float(clustered.value_counts().median())
                if not clustered.empty
                else 0.0
            ),
        }
    )

result = pd.DataFrame(rows)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print(result.to_string(index=False))
print()
print(f"Saved: {OUTPUT}")
