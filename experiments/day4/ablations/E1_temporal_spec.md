# Day 4 - E1 Temporal Ablation

## Purpose

E1 extends the frozen E0 thermal baseline with source-level temporal
behaviour.

## Frozen Temporal Features

- active_days
- temporal_span_days
- detection_frequency_per_day
- night_activity_ratio

## Auxiliary Temporal Feature

- day_activity_ratio

`day_activity_ratio` is retained for descriptive analysis but is not
included as an independent score component because it is complementary to
`night_activity_ratio`.

## Evaluation Population

- 35 clustered source-events
- DBSCAN noise events (`evt_noise_*`) excluded

## Ablation Rule

E1 = E0 thermal information + temporal behaviour.

The E0 source population, preprocessing and evaluation protocol remain fixed.

## Scientific Question

Does temporal persistence and activity behaviour provide additional
information beyond thermal intensity alone?

## Limitation

This is source-level behavioural characterization, not independently
verified industrial/environmental classification.

## Status

E1 FEATURE SET: FROZEN
