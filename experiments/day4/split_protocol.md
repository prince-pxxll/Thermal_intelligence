# Day 4 — Experimental Split Protocol

## Experimental Unit

The primary experimental unit is the source-event identified by `event_id`.

Each `event_id` is unique in the Day-3 feature table (160 unique events).

## Primary Evaluation Protocol

Because independently verified ground-truth labels are unavailable,
Day 4 does not use supervised train/test classification accuracy.

The E0-E4 experiments will use a fixed source-level evaluation partition
for comparative feature-ablation analysis.

The same partition must be used across E0, E1, E2, E3 and E4.

## Leakage Control

Feature groups will be defined before evaluation.

Geospatial context is treated as explanatory/contextual information
and not as ground truth.

## Temporal Limitation

The available dataset spans approximately 10 August 2026 through
8 September 2026.

Because 125 of 160 source-events contain exactly one spatial observation,
temporal generalization is considered a secondary robustness analysis
rather than the primary validation protocol.

## Source Distribution

- Total source-events: 160
- Single-observation source-events: 125
- Multi-observation source-events: 35
- Maximum observations for one source-event: 34

## Evaluation Principle

E0-E4 must use:

- identical source partition
- identical preprocessing
- identical evaluation procedure
- only the permitted information group changes between experiments

## Scientific Limitation

This protocol evaluates incremental information provided by thermal,
temporal, spatial, geospatial and historical features.

It does not establish externally verified real-world classification
accuracy for industrial versus environmental sources.

## Status

SPLIT PROTOCOL: FROZEN
PRIMARY UNIT: SOURCE-EVENT
GROUND-TRUTH CLASSIFICATION: NOT CLAIMED
