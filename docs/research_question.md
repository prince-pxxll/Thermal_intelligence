# Research Questions

## Primary question

> Given raw satellite thermal-anomaly detections over Maharashtra, can we reliably
> cluster, classify, and risk-score thermal events such that the output distinguishes
> routine/benign heat sources from anomalous or high-risk ones — with an explanation
> attached to each score?

## Supporting questions

1. **Detection quality** — What fraction of raw FIRMS detections over Maharashtra are
   likely false positives or low-confidence, and can we filter these reliably using
   confidence, brightness, and FRP (fire radiative power) fields?

2. **Spatiotemporal structure** — Do thermal detections form coherent spatiotemporal
   clusters (e.g. via DBSCAN/ST-DBSCAN), and do those clusters correspond to identifiable
   real-world events (a single fire, a burning season in one district, a recurring
   industrial source)?

3. **Persistence** — Can we define and compute a persistence score (recurrence over time
   at roughly the same location) that meaningfully separates one-off events from
   long-running or recurring thermal sources?

4. **Contextual classification** — Using OSM-derived land-use/infrastructure context
   (proximity to cropland, industrial zones, forest, urban areas), can we classify
   likely event *type* (agricultural burn, industrial, wildfire, other) with reasonable
   precision, in the absence of large labeled ground-truth sets?

5. **Anomaly detection** — Beyond classification, can unsupervised anomaly detection
   surface thermal events that don't fit expected seasonal/spatial patterns and thus
   warrant manual review?

6. **Risk scoring** — Can the above signals (confidence, persistence, context, anomaly
   score) be combined into a single, explainable risk score that is stable, interpretable,
   and useful for prioritization?

## Non-goals

- This project does **not** attempt to attribute legal responsibility for detected fires.
- This project does **not** claim causal identification of fire *cause* — outputs are
  probabilistic classifications, not forensic conclusions.
- Geographic scope is Maharashtra only; the pipeline is designed to be regionally
  configurable (see `config/regions/`) but is not validated elsewhere.

See [`limitations.md`](limitations.md) for a fuller discussion of scope boundaries.
