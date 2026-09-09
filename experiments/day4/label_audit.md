# Day 4 — Ground-Truth / Label Audit

## Objective

Determine whether the Day-3 source-level dataset contains independently
verified ground-truth labels suitable for supervised classification.

## Finding

No independent ground-truth target column was identified in
data/processed/feature_table.parquet.

The only semantically related field is:

- industrial_near_1km

This field is derived from:

distance_to_industry_m <= 1000 m

It represents contextual proximity to mapped industrial geometry,
not verified industrial-source ground truth.

Similarly:

- oad_near_1km is derived from distance_to_road_m
- armland_near_1km is derived from distance_to_farmland_m

These are geospatial context variables.

## Evaluation Decision

Because independently verified labels are not available, Day 4 will NOT
report supervised real-world classification accuracy.

Instead, validation will use:

1. Controlled E0-E4 ablation experiments
2. Anomaly/perturbation validation
3. Robustness and sensitivity analysis
4. Error/failure taxonomy
5. Explicit hypothesis-level evidence

## Scientific Limitation

Results will evaluate whether additional feature layers improve source
characterization and anomaly detection under the defined protocol.

They will not establish that the system correctly classifies every real-world
thermal source as industrial or environmental.

## Status

LABEL AUDIT: PASSED
GROUND TRUTH: NOT AVAILABLE
SUPERVISED ACCURACY: NOT CLAIMED
