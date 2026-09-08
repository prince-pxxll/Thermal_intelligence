from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "feature_table.parquet"
OUTPUT = ROOT / "data" / "processed" / "research_anomaly_scores.parquet"


FEATURES = [
    "max_frp",
    "max_brightness_ti4",
    "detection_frequency_per_day",
    "night_activity_ratio",
    "cluster_radius_km",
]


def robust_z(series):
    median = series.median()
    mad = (series - median).abs().median()

    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=series.index)

    return 0.6745 * (series - median) / mad


def main():

    df = pd.read_parquet(INPUT)

    # --------------------------------------------------
    # REAL DATA ONLY
    # --------------------------------------------------

    real = df[
        ~df["event_id"].str.startswith("evt_noise_")
    ].copy()

    print("=" * 60)
    print("THERMAL INTELLIGENCE — RESEARCH ANOMALY ENGINE")
    print("=" * 60)

    print(f"Total events: {len(df):,}")
    print(f"Real events:  {len(real):,}")
    print(
        f"Synthetic validation events: "
        f"{len(df) - len(real):,}"
    )

    # --------------------------------------------------
    # ROBUST COHORT BASELINES
    # --------------------------------------------------

    for feature in FEATURES:

        real[f"rz_{feature}"] = robust_z(
            real[feature]
        )

    # --------------------------------------------------
    # ANOMALY COMPONENTS
    # --------------------------------------------------

    real["thermal_anomaly"] = (
        real["rz_max_frp"].abs()
        + real["rz_max_brightness_ti4"].abs()
    ) / 2

    real["temporal_anomaly"] = (
        real["rz_detection_frequency_per_day"].abs()
        + real["rz_night_activity_ratio"].abs()
    ) / 2

    real["spatial_anomaly"] = (
        real["rz_cluster_radius_km"].abs()
    )

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    real["industrial_context"] = (
        real["distance_to_industry_m"] <= 1000
    ).astype(int)

    real["farmland_context"] = (
        real["distance_to_farmland_m"] <= 1000
    ).astype(int)

    real["road_context"] = (
        real["distance_to_road_m"] <= 1000
    ).astype(int)

    # --------------------------------------------------
    # CORE SCORE
    # --------------------------------------------------

    real["research_anomaly_raw"] = (
        0.50 * real["thermal_anomaly"]
        + 0.30 * real["temporal_anomaly"]
        + 0.20 * real["spatial_anomaly"]
    )

    # Percentile within REAL population only.
    real["research_anomaly_score"] = (
        real["research_anomaly_raw"]
        .rank(pct=True)
        * 100
    )

    real["research_anomaly_level"] = pd.cut(
        real["research_anomaly_score"],
        bins=[-np.inf, 50, 75, 90, np.inf],
        labels=[
            "normal",
            "elevated",
            "high",
            "extreme",
        ],
    )

    # --------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------

    def explain(row):

        reasons = []

        components = {
            "thermal intensity anomaly": row["thermal_anomaly"],
            "temporal activity anomaly": row["temporal_anomaly"],
            "spatial footprint anomaly": row["spatial_anomaly"],
        }

        # Strong anomaly drivers
        for name, value in components.items():
            if value >= 2:
                reasons.append(name)

        # If no strong driver exists, report the strongest contributor
        if not reasons:
            strongest = max(
                components,
                key=components.get,
            )

            reasons.append(
                f"moderate {strongest}"
            )

        # Environmental / geographic context
        if row["industrial_context"]:
            reasons.append("near industrial land use")

        if row["farmland_context"]:
            reasons.append("near farmland")

        if row["road_context"]:
            reasons.append("near major road")

        return "; ".join(reasons)

    real["anomaly_explanation"] = real.apply(
        explain,
        axis=1,
    )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    real.to_parquet(
        OUTPUT,
        index=False,
    )

    print()
    print(f"Saved: {OUTPUT}")

    print("\nAnomaly distribution:")
    print(
        real["research_anomaly_level"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nTop real anomalies:")

    print(
        real[
            [
                "event_id",
                "research_anomaly_score",
                "research_anomaly_level",
                "anomaly_explanation",
            ]
        ]
        .sort_values(
            "research_anomaly_score",
            ascending=False,
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()