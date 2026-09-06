# Limitations

## Data limitations

- **Satellite revisit gaps**: MODIS/VIIRS overpasses do not provide continuous
  coverage; short-lived thermal events between overpasses can be missed entirely.
- **Cloud and smoke obscuration**: heavy cloud cover or dense smoke can suppress
  detection, undercounting events during monsoon-adjacent periods or large fire events.
- **Spatial resolution**: at 375m–1km per pixel, multiple nearby small sources can
  appear as a single detection, and precise sub-pixel localization (e.g. which specific
  field or facility) is not possible from FIRMS data alone.
- **OSM completeness varies by district**: rural and less-mapped areas may lack
  industrial/land-use tagging, weakening contextual features there specifically.
- **Label scarcity**: ground-truth labels for event type (agricultural vs. industrial
  vs. wildfire) are sparse and unevenly distributed, limiting supervised model
  generalization and making reported classification metrics optimistic relative to
  true out-of-sample performance in under-labeled districts.

## Methodological limitations

- **Clustering sensitivity**: spatiotemporal clustering results (event boundaries,
  counts) are sensitive to the chosen spatial/temporal thresholds; different
  reasonable parameter choices can materially change cluster counts.
- **Persistence proxy imperfection**: the fixed-radius persistence buffer can conflate
  genuinely distinct nearby sources, or split a single large/moving source into
  multiple "events."
- **Anomaly ≠ risk**: statistical anomalies relative to seasonal baselines are not
  automatically dangerous or illegal; anomaly scores should be treated as a
  prioritization signal, not a conclusion.
- **No causal attribution**: nothing in this pipeline establishes legal responsibility,
  intent, or root cause for a given thermal event.

## Operational limitations

- **Not real-time**: the current pipeline is designed for batch/periodic runs, not
  streaming/real-time alerting, though the architecture does not preclude a future
  streaming mode.
- **Regional specificity**: thresholds, context weights, and validated behavior are
  tuned to Maharashtra; applying this pipeline to another region requires
  re-validation, not just a config swap.
- **API dependency**: the pipeline depends on the continued availability and terms of
  NASA FIRMS, Copernicus, and OSM/Overpass APIs; rate limits or API changes can disrupt
  ingestion.

## Ethical / usage considerations

- Risk scores are decision-support signals, not enforcement determinations. Any
  downstream action (e.g. regulatory follow-up) should involve independent
  verification (e.g. Sentinel imagery review, ground inspection) before action is
  taken against a specific location or party.
- Because OSM completeness and labeling density vary by area (often correlating with
  rural/urban and socio-economic factors), risk scores may be systematically less
  reliable in under-mapped regions — this should be disclosed alongside any published
  output, not hidden as false precision.
