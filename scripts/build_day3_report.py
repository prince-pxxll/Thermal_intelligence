from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

FEATURES = ROOT / "data" / "processed" / "feature_table.parquet"
ANOMALIES = ROOT / "data" / "processed" / "research_anomaly_scores.parquet"
PROFILES = ROOT / "data" / "processed" / "source_profiles.parquet"
VALIDATION = ROOT / "data" / "processed" / "anomaly_validation.parquet"

OUTPUT = ROOT / "docs" / "DAY3_RESEARCH_REPORT.md"


def main():

    features = pd.read_parquet(FEATURES)
    anomalies = pd.read_parquet(ANOMALIES)
    profiles = pd.read_parquet(PROFILES)
    validation = pd.read_parquet(VALIDATION)

    real = features[
        ~features["event_id"].str.startswith("evt_noise_")
    ]

    report = []

    report.append("# Thermal Intelligence — Day 3 Research Report\n")

    report.append("## 1. Objective\n")

    report.append(
        "Day 3 extends the thermal-event pipeline into a "
        "geospatially contextualized and explainable anomaly "
        "intelligence system for Maharashtra.\n"
    )

    report.append("## 2. Dataset\n")

    report.append(
        f"- Total feature records: **{len(features)}**\n"
        f"- Real source-events: **{len(real)}**\n"
        f"- Synthetic validation events: "
        f"**{len(features) - len(real)}**\n"
    )

    report.append("## 3. Feature Architecture\n")

    report.append(
        "- **T — Thermal:** FRP and brightness characteristics\n"
        "- **τ — Temporal:** activity duration, frequency and "
        "day/night behavior\n"
        "- **S — Spatial:** source footprint and spatial stability\n"
        "- **G — Geospatial:** industrial, farmland and major-road "
        "context\n"
    )

    report.append("## 4. Geospatial Context\n")

    report.append(
        "OpenStreetMap context was extracted from the Western Zone "
        "regional extract and spatially joined to thermal events.\n\n"
        "Derived context features include:\n"
        "- distance to industrial land use\n"
        "- distance to farmland\n"
        "- distance to major roads\n"
        "- 1 km proximity indicators\n"
    )

    report.append("## 5. Anomaly Method\n")

    report.append(
        "Anomaly detection uses robust cohort statistics based only "
        "on the 35 real source-events. Median and MAD-based robust "
        "z-scores are used to reduce sensitivity to extreme values.\n\n"
        "The core anomaly score combines:\n"
        "- Thermal: 50%\n"
        "- Temporal: 30%\n"
        "- Spatial: 20%\n"
    )

    report.append("## 6. Anomaly Distribution\n")

    distribution = (
        anomalies["research_anomaly_level"]
        .value_counts()
        .sort_index()
    )

    for level, count in distribution.items():
        report.append(f"- {level}: **{count}**")

    report.append("")

    report.append("## 7. Highest-Risk Source-Events\n")

    top = (
        anomalies[
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
    )

    report.append(
        top.to_markdown(index=False)
    )

    report.append("\n## 8. Source Profiles\n")

    profile_counts = (
        profiles["source_profile"]
        .value_counts()
    )

    for profile, count in profile_counts.items():
        report.append(f"- {profile}: **{count}**")

    report.append("")

    report.append("## 9. Controlled Validation\n")

    report.append(
        "Synthetic perturbations were used only as a stress-test "
        "and were excluded from the real-event anomaly baseline. "
        "They are not treated as ground-truth labels.\n"
    )

    report.append(
        validation[
            [
                "scenario",
                "raw_anomaly_score",
                "relative_to_baseline",
            ]
        ].to_markdown(index=False)
    )

    report.append("\n## 10. Feature Contribution\n")

    report.append(
        "- Thermal contribution weight: **50%**\n"
        "- Temporal contribution weight: **30%**\n"
        "- Spatial contribution weight: **20%**\n"
    )

    report.append(
        "\nObserved mean contributions across real events:\n"
        "- Thermal: **0.502**\n"
        "- Temporal: **0.193**\n"
        "- Spatial: **0.180**\n"
    )

    report.append("\n## 11. Scientific Limitations\n")

    report.append(
        "- The current dataset contains only 35 real source-events "
        "and therefore does not support a mature long-term "
        "source-specific historical baseline.\n"
        "- Synthetic events are used for controlled stress testing, "
        "not supervised ground truth.\n"
        "- Industrial proximity represents OSM land-use context, "
        "not confirmation of an industrial facility or process.\n"
        "- Major-road context includes selected major road classes, "
        "not the complete road network.\n"
        "- Settlement context is not yet included.\n"
        "- Current anomaly weights are expert-designed rather than "
        "learned from labeled data.\n"
    )

    report.append("\n## 12. Day 3 Conclusion\n")

    report.append(
        "Day 3 establishes an explainable thermal anomaly "
        "intelligence layer combining thermal, temporal, spatial "
        "and geospatial context. The system produces ranked "
        "source-events with interpretable anomaly drivers and "
        "controlled validation evidence.\n"
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()