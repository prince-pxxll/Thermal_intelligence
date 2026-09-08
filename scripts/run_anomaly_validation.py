from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "feature_table.parquet"
OUTPUT = ROOT / "data" / "processed" / "anomaly_validation.parquet"


FEATURES = [
    "max_frp",
    "max_brightness_ti4",
    "detection_frequency_per_day",
    "night_activity_ratio",
    "cluster_radius_km",
]


def robust_z(value, reference):

    median = reference.median()
    mad = (reference - median).abs().median()

    if mad == 0:
        return 0.0

    return 0.6745 * (value - median) / mad


def calculate_score(row, reference):

    thermal = np.mean([
        abs(robust_z(row["max_frp"], reference["max_frp"])),
        abs(
            robust_z(
                row["max_brightness_ti4"],
                reference["max_brightness_ti4"],
            )
        ),
    ])

    temporal = np.mean([
        abs(
            robust_z(
                row["detection_frequency_per_day"],
                reference["detection_frequency_per_day"],
            )
        ),
        abs(
            robust_z(
                row["night_activity_ratio"],
                reference["night_activity_ratio"],
            )
        ),
    ])

    spatial = abs(
        robust_z(
            row["cluster_radius_km"],
            reference["cluster_radius_km"],
        )
    )

    return (
        0.50 * thermal
        + 0.30 * temporal
        + 0.20 * spatial
    )


def main():

    df = pd.read_parquet(INPUT)

    real = df[
        ~df["event_id"].str.startswith("evt_noise_")
    ].copy()

    print("=" * 60)
    print("ANOMALY DETECTOR — CONTROLLED VALIDATION")
    print("=" * 60)

    scenarios = []

    baseline = real.median(numeric_only=True)

    scenarios.append(
        {
            "scenario": "baseline",
            "max_frp": baseline["max_frp"],
            "max_brightness_ti4": baseline["max_brightness_ti4"],
            "detection_frequency_per_day": baseline[
                "detection_frequency_per_day"
            ],
            "night_activity_ratio": baseline[
                "night_activity_ratio"
            ],
            "cluster_radius_km": baseline[
                "cluster_radius_km"
            ],
        }
    )

    # --------------------------------------------------
    # CONTROLLED PERTURBATIONS
    # --------------------------------------------------

    tests = {
        "high_frp": {
            "max_frp": real["max_frp"].quantile(0.95)
        },
        "high_brightness": {
            "max_brightness_ti4":
                real["max_brightness_ti4"].quantile(0.95)
        },
        "high_frequency": {
            "detection_frequency_per_day":
                real["detection_frequency_per_day"].quantile(0.95)
        },
        "high_night_activity": {
            "night_activity_ratio": 1.0
        },
        "large_spatial_footprint": {
            "cluster_radius_km":
                real["cluster_radius_km"].quantile(0.95)
        },
        "combined_extreme": {
            "max_frp":
                real["max_frp"].quantile(0.99),
            "max_brightness_ti4":
                real["max_brightness_ti4"].quantile(0.99),
            "detection_frequency_per_day":
                real["detection_frequency_per_day"].quantile(0.99),
            "night_activity_ratio": 1.0,
            "cluster_radius_km":
                real["cluster_radius_km"].quantile(0.99),
        },
    }

    for name, changes in tests.items():

        row = baseline.copy()

        for feature, value in changes.items():
            row[feature] = value

        scenarios.append(
            {
                "scenario": name,
                **{
                    feature: row[feature]
                    for feature in FEATURES
                },
            }
        )

    validation = pd.DataFrame(scenarios)

    validation["raw_anomaly_score"] = validation.apply(
        lambda row: calculate_score(
            row,
            real[FEATURES],
        ),
        axis=1,
    )

    validation["relative_to_baseline"] = (
        validation["raw_anomaly_score"]
        - validation.loc[
            validation["scenario"] == "baseline",
            "raw_anomaly_score",
        ].iloc[0]
    )

    validation.to_parquet(
        OUTPUT,
        index=False,
    )

    print("\nValidation results:\n")

    print(
        validation[
            [
                "scenario",
                "raw_anomaly_score",
                "relative_to_baseline",
            ]
        ].to_string(index=False)
    )

    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()