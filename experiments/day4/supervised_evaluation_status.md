# Day 4 - Supervised Evaluation Status

## Status

Supervised classification evaluation is not executable on the current
repository state.

## Missing Inputs

- No ground-truth label dataset exists under `data/labels/`.
- No trained classification model exists under `models/`.
- No model predictions exist under `results/`.
- The current feature table contains source-event features but no verified
  class labels.

## Therefore Not Reported

The following metrics are intentionally not fabricated:

- confusion matrix
- precision
- recall
- F1
- ROC-AUC
- PR-AUC
- calibration error

## Why DBSCAN Noise Is Not Used as Ground Truth

Events named `evt_noise_*` are produced when the frozen spatiotemporal
DBSCAN assigns a point the noise label (-1). These events are source-
formation outputs, not independently verified environmental or
non-industrial labels.

## Required Future Input

A valid supervised evaluation requires an independently defined and
documented label set for the target classification task, followed by
leakage-safe train/test evaluation and prediction generation.

## Current Scientific Status

The Day 4 ablation and robustness experiments are complete.

The supervised classification evaluation is BLOCKED BY LABEL AVAILABILITY,
not omitted silently.

No unsupported accuracy or classification claim is made.
