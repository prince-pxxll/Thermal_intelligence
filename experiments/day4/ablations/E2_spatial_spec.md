# Day 4 - E2 Spatial Ablation

## Purpose

E2 extends the frozen E1 thermal + temporal baseline with spatial
structure of each source-event.

## Spatial Score Features

- cluster_radius_km
- spatial_std_km
- spatial_observations

## Auxiliary Spatial Fields

- centroid_lat
- centroid_lon

Centroid coordinates are retained for geographic description but are not
used as independent anomaly-score components.

## Evaluation Population

- 35 clustered source-events
- DBSCAN noise events (`evt_noise_*`) excluded

## Ablation Rule

E2 = E1 + spatial structure.

The source population, preprocessing and evaluation protocol remain fixed.

## Scientific Question

Does spatial structure provide additional information beyond thermal and
temporal behaviour?

## Limitation

This is source-level characterization, not independently verified
industrial/environmental classification.

## Status

E2 FEATURE SET: FROZEN
