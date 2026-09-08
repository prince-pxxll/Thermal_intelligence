from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

REPRESENTATION = (
    ROOT
    / "experiments"
    / "clustering"
    / "h3_representation_comparison_v2.csv"
)

COVERAGE = (
    ROOT
    / "experiments"
    / "clustering"
    / "h3_coverage_sensitivity.csv"
)

OUTPUT = (
    ROOT
    / "experiments"
    / "clustering"
    / "h3_summary.csv"
)


def main():
    representation = pd.read_csv(REPRESENTATION)
    coverage = pd.read_csv(COVERAGE)

    baseline = coverage[coverage["config"] == "C5"].iloc[0]

    summary = pd.DataFrame(
        [
            {
                "hypothesis": "H3",
                "individual_observations": int(
                    representation.loc[
                        representation["representation"]
                        == "individual_observation",
                        "analytical_units",
                    ].iloc[0]
                ),
                "source_level_events": int(
                    representation.loc[
                        representation["representation"]
                        == "source_level_event",
                        "analytical_units",
                    ].iloc[0]
                ),
                "baseline_source_coverage": float(
                    baseline["observation_coverage_fraction"]
                ),
                "baseline_observations_represented": int(
                    baseline["observations_represented"]
                ),
                "baseline_observations_total": int(
                    baseline["total_observations"]
                ),
                "recurring_source_fraction": float(
                    representation.loc[
                        representation["representation"]
                        == "source_level_event",
                        "recurring_unit_fraction",
                    ].iloc[0]
                ),
                "persistent_source_fraction": float(
                    representation.loc[
                        representation["representation"]
                        == "source_level_event",
                        "persistent_unit_fraction",
                    ].iloc[0]
                ),
                "mean_source_radius_km": float(
                    representation.loc[
                        representation["representation"]
                        == "source_level_event",
                        "mean_spatial_radius_km",
                    ].iloc[0]
                ),
                "interpretation": "Partial support; source-level representation reveals recurrence and persistence, but clustering coverage is parameter-sensitive.",
            }
        ]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT, index=False)

    print("\nH3 Summary")
    print(summary.to_string(index=False))
    print(f"\nSaved to: {OUTPUT}")


if __name__ == "__main__":
    main()