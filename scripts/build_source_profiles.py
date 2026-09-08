from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "research_anomaly_scores.parquet"
OUTPUT = ROOT / "data" / "processed" / "source_profiles.parquet"


def classify_source(row):

    industrial = row["industrial_context"] == 1
    farmland = row["farmland_context"] == 1

    anomaly = row["research_anomaly_score"]

    if industrial and anomaly >= 75:
        return "industrial-like_high-risk"

    if farmland and anomaly >= 75:
        return "agricultural-like_high-risk"

    if industrial:
        return "industrial-context"

    if farmland:
        return "agricultural-context"

    if anomaly >= 90:
        return "high-anomaly_unknown-context"

    if anomaly >= 75:
        return "elevated-anomaly_unknown-context"

    return "background-thermal-source"


def main():

    df = pd.read_parquet(INPUT)

    print("=" * 60)
    print("THERMAL INTELLIGENCE — SOURCE PROFILE ENGINE")
    print("=" * 60)

    df["source_profile"] = df.apply(
        classify_source,
        axis=1,
    )

    # Compact research-facing profile table
    columns = [
        "event_id",

        # Thermal fingerprint
        "mean_frp",
        "median_frp",
        "max_frp",
        "frp_std",
        "mean_brightness_ti4",
        "max_brightness_ti4",

        # Temporal fingerprint
        "active_days",
        "temporal_span_days",
        "detection_frequency_per_day",
        "night_activity_ratio",
        "day_activity_ratio",

        # Spatial fingerprint
        "cluster_radius_km",
        "spatial_std_km",
        "spatial_observations",

        # Geospatial context
        "distance_to_industry_m",
        "distance_to_road_m",
        "distance_to_farmland_m",
        "industrial_context",
        "road_context",
        "farmland_context",

        # Intelligence
        "research_anomaly_score",
        "research_anomaly_level",
        "anomaly_explanation",
        "source_profile",
    ]

    profile = df[columns].copy()

    profile.to_parquet(
        OUTPUT,
        index=False,
    )

    print(f"\nProfiles created: {len(profile)}")
    print(f"Saved: {OUTPUT}")

    print("\nSource profile distribution:")
    print(
        profile["source_profile"]
        .value_counts()
        .to_string()
    )

    print("\nTop high-risk profiles:")

    print(
        profile[
            [
                "event_id",
                "research_anomaly_score",
                "source_profile",
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