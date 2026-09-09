# Day 4 — E0 Raw Thermal Baseline

## Purpose

E0 is the minimum-information thermal baseline.

It evaluates source characterization using thermal observations only,
without temporal, spatial, geospatial-context, or historical features.

## Frozen Features

- mean_frp
- median_frp
- max_frp
- mean_brightness_ti4
- max_brightness_ti4
- mean_brightness_ti5
- confidence_high_ratio

## Excluded Feature

`frp_std` is excluded because it is missing for 125 of 160 source-events
(78.125% of the dataset).

No imputation is introduced for E0.

## Dataset

- Source-events: 160
- Complete E0 feature rows: 160
- Missing E0 values: 0

## Scientific Role

E0 establishes the performance/behaviour of the thermal information layer
before adding temporal, spatial, geospatial, or historical information.

This is an ablation baseline, not independently verified real-world
classification accuracy.

## Status

E0 FEATURE SET: FROZEN
