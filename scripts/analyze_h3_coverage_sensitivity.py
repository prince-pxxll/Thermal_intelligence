from pathlib import Path

import pandas as pd

from thermal_intelligence.geospatial.clustering import st_dbscan


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "interim" / "clustering_input.parquet"
OUTPUT = ROOT / "experiments" / "clustering" / "h3_coverage_sensitivity.csv"


CONFIGS = [
    {
        "config": "C1",
        "spatial_eps_km": 0.25,
        "temporal_eps_hours": 24,
        "min_samples": 2,
    },
    {
        "config": "C2",
        "spatial_eps_km": 0.50,
        "temporal_eps_hours": 24,
        "min_samples": 2,
    },
    {
        "config": "C3",
        "spatial_eps_km": 0.50,
        "temporal_eps_hours": 48,
        "min_samples": 3,
    },
    {
        "config": "C4",
        "spatial_eps_km": 0.75,
        "temporal_eps_hours": 48,
        "min_samples": 3,
    },
    {
        "config": "C5",
        "spatial_eps_km": 1.00,
        "temporal_eps_hours": 48,
        "min_samples": 2,
    },
    {
        "config": "C6",
        "spatial_eps_km": 1.00,
        "temporal_eps_hours": 72,
        "min_samples": 3,
    },
]


def main():
    df = pd.read_parquet(INPUT)

    total_observations = len(df)

    results = []

    for cfg in CONFIGS:
        clustered = st_dbscan(
            df,
            spatial_eps_km=cfg["spatial_eps_km"],
            temporal_eps_hours=cfg["temporal_eps_hours"],
            min_samples=cfg["min_samples"],
        )

        counts = clustered[clustered != -1].value_counts()

        multi_point_ids = counts[counts > 1].index

        represented = int(
            clustered.isin(multi_point_ids).sum()
        )

        coverage = represented / total_observations

        results.append(
            {
                "config": cfg["config"],
                "spatial_eps_km": cfg["spatial_eps_km"],
                "temporal_eps_hours": cfg["temporal_eps_hours"],
                "min_samples": cfg["min_samples"],
                "total_observations": total_observations,
                "multi_observation_clusters": len(multi_point_ids),
                "observations_represented": represented,
                "observation_coverage_fraction": coverage,
                "singleton_or_noise_observations": (
                    total_observations - represented
                ),
            }
        )

    result_df = pd.DataFrame(results)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUTPUT, index=False)

    print("\nH3 clustering coverage sensitivity")
    print(result_df.to_string(index=False))
    print(f"\nSaved to: {OUTPUT}")


if __name__ == "__main__":
    main()