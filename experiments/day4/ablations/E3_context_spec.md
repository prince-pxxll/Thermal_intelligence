# Day 4 - E3 Geospatial Context Ablation

## Purpose

E3 extends the frozen E2 thermal + temporal + spatial baseline with
geospatial context.

## Geospatial Score Features

- distance_to_industry_m
- distance_to_road_m
- distance_to_farmland_m

Distances are transformed into contextual proximity scores during scoring.

## Auxiliary Context Flags

- industrial_near_1km
- road_near_1km
- farmland_near_1km

These are retained for interpretation but are not independently weighted
when the corresponding continuous distance is already used.

## Evaluation Population

- 35 clustered source-events
- DBSCAN noise events excluded

## Data Audit

All six geospatial fields are complete for the 35 evaluation events.

`farmland_near_1km` is constant at 0 across the evaluation population and
therefore provides no independent variation.

## Ablation Rule

E3 = E2 + geospatial context.

The source population, preprocessing and evaluation protocol remain fixed.

## Scientific Question

Does geospatial context change source prioritization beyond thermal,
temporal and spatial behaviour?

## Limitation

Mapped geospatial context is explanatory information, not independently
verified source classification.

## Status

E3 FEATURE SET: FROZEN
