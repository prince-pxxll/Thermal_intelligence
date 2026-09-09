# Day 4 - E0 Evaluation Population

## Population Definition

E0 is evaluated on the 35 clustered source-events produced by the frozen
ST-DBSCAN source-formation pipeline.

Events whose IDs begin with `evt_noise_` are DBSCAN noise points and are
excluded from the primary clustered-source evaluation population.

## Counts

- Total feature-table events: 160
- Clustered source-events: 35
- DBSCAN noise events: 125

## Important Interpretation

The clustered population is NOT ground truth for industrial sources.

The `evt_noise_*` population is NOT ground truth for environmental sources.

These populations reflect the source-formation algorithm and its data
construction, not independently verified class labels.

## E0 Role

E0 evaluates the behaviour of the thermal-only feature layer on the
clustered source-event population.

Synthetic/noise events remain available for separate controlled
source-formation validation.

## Status

E0 EVALUATION POPULATION: FROZEN
