import pandas as pd
from pathlib import Path

OBS = Path("data/interim/firms_preprocessed.parquet")
EVENTS = Path("data/processed/events_with_context.parquet")
SOURCES = Path("data/processed/thermal_sources.parquet")
OUTPUT = Path("experiments/clustering/h3_representation_comparison.csv")

obs = pd.read_parquet(OBS)
events = pd.read_parquet(EVENTS)
sources = pd.read_parquet(SOURCES)

# Approach A: individual detections.
approach_a = {
    "representation": "individual_observation",
    "n_rows": len(obs),
    "n_spatial_units": obs[["latitude", "longitude"]].drop_duplicates().shape[0],
    "n_temporal_units": obs["acq_datetime_ist"].dt.date.nunique(),
    "mean_frp": obs["frp"].mean(),
    "frp_std": obs["frp"].std(),
    "mean_active_days_per_unit": 1.0,
}

# Approach B: multi-observation clustered events only.
multi = sources[sources["n_observations"] > 1].copy()

approach_b = {
    "representation": "source_level_event",
    "n_rows": len(multi),
    "n_spatial_units": len(multi),
    "n_temporal_units": int(multi["active_days"].sum()),
    "mean_frp": multi["mean_frp"].mean(),
    "frp_std": multi["mean_frp"].std(),
    "mean_active_days_per_unit": multi["active_days"].mean(),
}

result = pd.DataFrame([approach_a, approach_b])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("H3 representation comparison")
print()
print(result.to_string(index=False))
print()
print(f"Saved: {OUTPUT}")
