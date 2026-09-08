# Assumptions

This document records working assumptions made throughout the pipeline. Assumptions
should be revisited as data and validation accumulate; when one changes, update this
file and note the change via an ADR in `docs/decisions/`.

## Data assumptions

- FIRMS detections with `confidence = low` are excluded from the current cleaned
  dataset because the pipeline currently applies a minimum confidence threshold of
  `nominal`. This is a configurable preprocessing choice and should be revisited
  if confidence weighting is introduced later.
- VIIRS detections (375m) are treated as higher spatial fidelity than MODIS (1km) when
  both are available for the same event; MODIS is used primarily for temporal backfill
  before VIIRS coverage was consistent.
- OSM land-use tagging in Maharashtra is assumed to be incomplete in rural areas;
  absence of a tagged feature (e.g. no tagged industrial polygon) is not treated as
  strong evidence of absence.
- Sentinel imagery cloud cover is assumed to intermittently block visual confirmation;
  the pipeline does not require Sentinel confirmation for a detection to be scored, only
  for optional manual review.

## Modeling assumptions

- Spatiotemporal clustering assumes thermal events are approximately stationary over
  the clustering time window (default: same-day to multi-day, configurable) — i.e. we
  are not attempting to track a moving fire front pixel-by-pixel.
- Persistence scoring assumes a fixed spatial buffer radius (configurable in
  `config/features/feature_schema.yaml`) is a reasonable proxy for "same source" across
  repeated detections; this is a simplification and may merge distinct nearby sources.
- Event-type classification assumes the available label set (`data/labels/`), where
  present, is representative enough to generalize across districts; this is a known
  weak point given likely regional labeling gaps (see `limitations.md`).
- Anomaly detection assumes "normal" seasonal/spatial patterns are learnable from
  historical FIRMS data over Maharashtra and that deviations from this baseline are
  more likely to warrant attention — this does not imply deviations are necessarily
  harmful or illegal.

## Scope assumptions

- Time zone: all timestamps are normalized to IST (UTC+5:30) for feature
  engineering and reporting, even though raw FIRMS timestamps are UTC.
- Coordinate reference system: EPSG:4326 for storage/interchange; projected CRS
  (EPSG:32643, UTM zone 43N) used internally for distance/area calculations.
- The Maharashtra state boundary from the official Survey of India administrative
  boundary dataset is used as the authoritative spatial boundary for filtering.
  `config/regions/maharashtra.yaml` provides the project region configuration and
  coarse geographic scope.
