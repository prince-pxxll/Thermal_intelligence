from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "feature_table.parquet"
OUTPUT = ROOT / "data" / "processed" / "anomaly_scores.parquet"


FEATURES = {
    "thermal_intensity": "max_frp",
    "thermal_brightness": "max_brightness_ti4",
    "detection_frequency": "detection_frequency_per_day",
    "night_activity": "night_activity_ratio",
    "spatial_footprint": "cluster_radius_km",
    "industry_distance": "distance_to_industry_m",
    "farmland_distance": "distance_to_farmland_m",
}


def robust_z(series):
    """Robust z-score using median and MAD."""
    x = pd.to_numeric(series, errors="coerce")

    median = x.median()
    mad = (x - median).abs().median()

    if pd.isna(mad) or mad == 0:
        return pd.Series(0.0, index=x.index)

    return 0.6745 * (x - median) / mad


def main():

    df = pd.read_parquet(INPUT)

    print("=" * 60)
    print("DAY 3 — THERMAL INTELLIGENCE ANOMALY ENGINE")
    print("=" * 60)

    # --------------------------------------------------
    # Robust anomaly components
    # --------------------------------------------------

    df["anomaly_frp"] = robust_z(
        df["max_frp"]
    ).abs()

    df["anomaly_brightness"] = robust_z(
        df["max_brightness_ti4"]
    ).abs()

    df["anomaly_frequency"] = robust_z(
        df["detection_frequency_per_day"]
    ).abs()

    df["anomaly_night_activity"] = robust_z(
        df["night_activity_ratio"]
    ).abs()

    df["anomaly_spatial"] = robust_z(
        df["cluster_radius_km"]
    ).abs()

    # --------------------------------------------------
    # Context signals
    # --------------------------------------------------

    # Close industrial proximity is contextual,
    # NOT automatically anomalous.
    industry_proximity = 1 / (
        1 + df["distance_to_industry_m"] / 1000
    )

    farmland_proximity = 1 / (
        1 + df["distance_to_farmland_m"] / 1000
    )

    df["industry_proximity_score"] = industry_proximity
    df["farmland_proximity_score"] = farmland_proximity

    # --------------------------------------------------
    # Core anomaly score
    # --------------------------------------------------

    components = [
        "anomaly_frp",
        "anomaly_brightness",
        "anomaly_frequency",
        "anomaly_night_activity",
        "anomaly_spatial",
    ]

    df["anomaly_score_raw"] = df[components].mean(axis=1)

    # Convert to 0–100 percentile score.
    df["anomaly_score"] = (
        df["anomaly_score_raw"]
        .rank(pct=True)
        * 100
    )

    # --------------------------------------------------
    # Severity
    # --------------------------------------------------

    df["anomaly_level"] = pd.cut(
        df["anomaly_score"],
        bins=[-np.inf, 50, 75, 90, np.inf],
        labels=[
            "normal",
            "elevated",
            "high",
            "extreme",
        ],
    )

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    def explain(row):

        reasons = []

        if row["anomaly_frp"] >= 2:
            reasons.append("unusually high FRP")

        if row["anomaly_brightness"] >= 2:
            reasons.append("unusual thermal brightness")

        if row["anomaly_frequency"] >= 2:
            reasons.append("unusual detection frequency")

        if row["anomaly_night_activity"] >= 2:
            reasons.append("unusual night activity")

        if row["anomaly_spatial"] >= 2:
            reasons.append("unusual spatial footprint")

        if row["distance_to_industry_m"] <= 1000:
            reasons.append("near industrial land use")

        if row["distance_to_farmland_m"] <= 1000:
            reasons.append("near farmland")

        if not reasons:
            reasons.append("no dominant anomaly driver")

        return "; ".join(reasons)

    df["anomaly_explanation"] = df.apply(
        explain,
        axis=1,
    )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    df.to_parquet(
        OUTPUT,
        index=False,
    )

    print()
    print(f"Events: {len(df):,}")
    print(f"Saved: {OUTPUT}")

    print()
    print("Anomaly levels:")
    print(
        df["anomaly_level"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print()
    print("Score statistics:")
    print(
        df["anomaly_score"]
        .describe()
        .to_string()
    )

    print()
    print("Top 10 anomalies:")

    print(
        df[
            [
                "event_id",
                "anomaly_score",
                "anomaly_level",
                "anomaly_explanation",
            ]
        ]
        .sort_values(
            "anomaly_score",
            ascending=False,
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
    