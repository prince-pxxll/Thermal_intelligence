# Day 4 - E4 Historical Behaviour

## Status

E4 is not executed in the current dataset.

## Reason

The Day-3 feature table contains no independently defined historical
baseline, recurrence, trend, or prior-period deviation feature.

The available temporal variables:

- first_seen
- last_seen
- active_days
- temporal_span_days
- detection_frequency_per_day
- night_activity_ratio
- day_activity_ratio

are already used by E1 and therefore cannot be reused as an independent
historical layer without double-counting information.

## Scientific Decision

No synthetic historical feature will be invented.

No E4 score will be reported.

## Future Extension

A valid E4 layer would require additional longitudinal observations
outside the current source-event construction, allowing comparison of a
source against its prior historical behaviour.

## Current Ablation Ladder

E0 = Thermal
E1 = Thermal + Temporal
E2 = Thermal + Temporal + Spatial
E3 = Thermal + Temporal + Spatial + Geospatial
E4 = Not available in current data

## Status

E4: DEFERRED
REASON: NO HISTORICAL FEATURE AVAILABLE
NO FABRICATED RESULT
