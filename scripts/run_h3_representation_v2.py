import pandas as pd
from pathlib import Path

OBS = Path("data/interim/firms_preprocessed.parquet")
SOURCES = Path("data/processed/thermal_sources.parquet")
OUTPUT = Path("experiments/clustering/h3_representation_comparison_v2.csv")

obs = pd.read_parquet(OBS)
sources = pd.read_parquet(SOURCES)

# -------------------------
# Approach A: observations
# -------------------------
observation_unit_count = len(obs)

observation_unique_dates = obs["acq_datetime_ist"].dt.date.nunique()

observation_mean_frp = obs["frp"].mean()
observation_frp_std = obs["frp"].std()

# -------------------------
# Approach B: source events
# Multi-observation events only
# -------------------------
multi = sources[sources["n_observations"] > 1].copy()

source_unit_count = len(multi)

source_total_active_days = multi["active_days"].sum()
source_mean_active_days = multi["active_days"].mean()

source_mean_frp = multi["mean_frp"].mean()
source_frp_std = multi["mean_frp"].std()

source_mean_radius = multi["cluster_radius_km"].mean()
source_median_radius = multi["cluster_radius_km"].median()

# Concentration / recurrence metrics
observations_represented = int(multi["n_observations"].sum())
representation_fraction = observations_represented / len(obs)

recurring_source_fraction = (
    multi["active_days"].ge(2).mean()
)

persistent_source_fraction = (
    multi["active_days"].ge(3).mean()
)

result = pd.DataFrame(
    [
        {
            "representation": "individual_observation",
            "analytical_units": observation_unit_count,
            "unique_calendar_dates": observation_unique_dates,
            "mean_frp": observation_mean_frp,
            "frp_std": observation_frp_std,
            "mean_active_days_per_unit": 1.0,
            "mean_spatial_radius_km": None,
            "observations_represented": observation_unit_count,
            "observation_representation_fraction": 1.0,
            "recurring_unit_fraction": None,
            "persistent_unit_fraction": None,
        },
        {
            "representation": "source_level_event",
            "analytical_units": source_unit_count,
            "unique_calendar_dates": None,
            "mean_frp": source_mean_frp,
            "frp_std": source_frp_std,
            "mean_active_days_per_unit": source_mean_active_days,
            "mean_spatial_radius_km": source_mean_radius,
            "observations_represented": observations_represented,
            "observation_representation_fraction": representation_fraction,
            "recurring_unit_fraction": recurring_source_fraction,
            "persistent_unit_fraction": persistent_source_fraction,
        },
    ]
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("H3 representation comparison v2")
print()
print(result.to_string(index=False))
print()
print("Source-level diagnostics")
print(f"Multi-observation sources: {source_unit_count}")
print(f"Observations represented by those sources: {observations_represented}")
print(f"Observation coverage: {representation_fraction:.4f}")
print(f"Recurring source fraction (>=2 active days): {recurring_source_fraction:.4f}")
print(f"Persistent source fraction (>=3 active days): {persistent_source_fraction:.4f}")
print(f"Mean source radius: {source_mean_radius:.4f} km")
print(f"Median source radius: {source_median_radius:.4f} km")
print()
print(f"Saved: {OUTPUT}")
