from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "experiments" / "day4" / "DAY4_REPORT.md"

summary = pd.read_csv(
    ROOT / "experiments" / "day4" / "ablation_comparison" / "score_summary.csv"
)

corr = pd.read_csv(
    ROOT / "experiments" / "day4" / "ablation_comparison" / "rank_correlations.csv"
)

robust = pd.read_csv(
    ROOT / "experiments" / "day4" / "robustness" / "weight_sensitivity.csv"
)

report = f"""# Day 4 - Ablation and Robustness Report

## 1. Objective

Evaluate how progressively adding thermal, temporal, spatial and
geospatial information changes source-level prioritization.

The analysis does not claim independently verified industrial/environmental
classification accuracy because independently verified ground-truth labels
are unavailable.

## 2. Evaluation Population

- Total feature-table events: 160
- Clustered source-events: 35
- DBSCAN noise events: 125
- Primary E0-E3 population: 35 clustered source-events

`evt_noise_*` events represent DBSCAN noise points and are not treated as
environmental ground truth.

## 3. Ablation Ladder

- E0 = thermal
- E1 = thermal + temporal
- E2 = thermal + temporal + spatial
- E3 = thermal + temporal + spatial + geospatial
- E4 = deferred because no independent historical feature exists

## 4. Ablation Summary

{summary.to_string(index=False)}

## 5. Rank Correlations

{corr.to_string(index=False)}

The complete E0-to-E3 ranking correlation is 0.7703, indicating that the
context-rich E3 prioritization is meaningfully different from the
thermal-only E0 prioritization while retaining partial ranking continuity.

## 6. Observed Incremental Effects

Temporal information materially re-ranked sources relative to E0.

Spatial information produced further substantial re-ranking relative to E1.

Geospatial context produced additional re-ranking while preserving strong
agreement with E2.

These effects demonstrate incremental information content under the fixed
ablation protocol. They do not establish classification accuracy.

## 7. Weight Sensitivity

{robust.to_string(index=False)}

The tested alternative weighting schemes produced Spearman correlations
of approximately 0.962 to 0.991 relative to the baseline E3 ranking.

This indicates that the tested ranking is relatively stable to the
moderate weight perturbations evaluated here.

## 8. Statistical Limitation

The frozen Day-3 robust-z implementation returns zero when the global MAD
of a feature is zero.

In the mixed 160-event population:

- detection_frequency_per_day: 81.25% at 1.0
- night_activity_ratio: 51.88% at 1.0
- cluster_radius_km: 78.12% at 0.0

Therefore these Day-3 anomaly components are inactive in the frozen
anomaly output.

This limitation was documented without modifying the Day-3 outputs.

## 9. Historical Layer

E4 was not executed.

The current feature table contains no independently defined historical
baseline, recurrence, trend or prior-period deviation feature.

No synthetic historical feature was invented.

## 10. Scientific Interpretation

The experiments support the hypothesis that thermal, temporal, spatial and
geospatial information provide distinct and incrementally changing source
characterization signals under the defined scoring framework.

The experiments do not demonstrate independently verified industrial versus
environmental classification performance.

## 11. Reproducibility

All E0-E3 artifacts, specifications, scoring scripts, ablation summaries,
and robustness outputs are stored under `experiments/day4/`.

## Status

DAY 4 ANALYSIS: COMPLETE
E0-E3: COMPLETE
E4: DEFERRED
GROUND-TRUTH CLASSIFICATION ACCURACY: NOT CLAIMED
ROBUSTNESS ANALYSIS: COMPLETE
"""

OUT.write_text(report, encoding="utf-8")

print("=" * 60)
print("DAY 4 - FINAL REPORT")
print("=" * 60)
print(f"Saved: {OUT}")
