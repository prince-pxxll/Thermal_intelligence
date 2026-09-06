# Methodology

## Overview

The pipeline moves through six stages, each corresponding to a package under
`src/thermal_intelligence/` and a stage script under `pipelines/`:

```
ingest -> preprocess -> geospatial context -> feature engineering -> modeling -> risk scoring
```

## 1. Ingestion (`data/firms.py`, `pipelines/ingest.py`)

- Pull active-fire detections from the NASA FIRMS API for the Maharashtra bounding box
  / administrative boundary, over a configurable date range.
- Persist raw responses unmodified to `data/raw/firms/` (immutable raw layer).
- Pull supplementary OSM extracts (land use, industrial zones, road network) to
  `data/raw/osm/`, and Sentinel-2/3 scenes where visual confirmation is needed to
  `data/raw/sentinel/`.

## 2. Validation & preprocessing (`data/validation.py`, `data/preprocessing.py`)

- Schema validation against `config/features/feature_schema.yaml`.
- Deduplication of overlapping satellite passes.
- Confidence/quality filtering (drop low-confidence detections unless explicitly
  retained for anomaly analysis).
- Coordinate reference system normalization (all geometries to EPSG:4326 for storage,
  reprojected as needed for distance calculations).
- Output written to `data/interim/`.

## 3. Geospatial context (`geospatial/`)

- **Clustering** (`clustering.py`): spatiotemporal clustering (ST-DBSCAN or similar) to
  group individual detections into coherent "events."
- **Distance** (`distance.py`): nearest-neighbor distance calculations to
  infrastructure, cropland boundaries, forest reserves, and urban areas.
- **OSM joins** (`osm.py`): spatial join of detections/clusters against OSM land-use
  and infrastructure polygons.
- **Spatial features** (`spatial_features.py`): derived features such as cluster
  density, distance-to-nearest-industrial-site, land-use category at centroid.

## 4. Feature engineering (`features/`)

- **Thermal** (`thermal.py`): brightness temperature, FRP, day/night flag, satellite
  source.
- **Temporal** (`temporal.py`): time-of-day, day-of-year/season, detection frequency.
- **Persistence** (`persistence.py`): recurrence of detections within a spatial buffer
  over a rolling time window; distinguishes one-off vs. recurring sources.
- **Context** (`context.py`): combines geospatial context features into a unified
  per-event feature vector, per `config/features/feature_schema.yaml`.

## 5. Modeling (`models/`)

- **Classification** (`classification.py`): supervised or weak-supervised event-type
  classification (agricultural / industrial / wildfire / other) where labels are
  available (`data/labels/`).
- **Anomaly detection** (`anomaly.py`): unsupervised methods (e.g. isolation forest,
  local outlier factor) to flag statistically unusual events independent of the
  classifier.
- **Evaluation** (`evaluation.py`): shared metrics (precision/recall/F1 for
  classification; precision@k, silhouette-based cluster validity for
  clustering/anomaly detection).

## 6. Risk scoring (`risk/`)

- **Scoring** (`scoring.py`): combines classification confidence, persistence score,
  anomaly score, and contextual severity weights into a single 0–100 risk score per
  event.
- **Explanation** (`explanation.py`): generates a human-readable rationale per score
  (e.g. "High risk: recurring detection (11 days), 240m from industrial zone, flagged
  as anomalous relative to seasonal baseline").

## Evaluation strategy

- Baseline models and ablations are tracked under `experiments/`.
- Metrics, figures, and generated reports land in `results/`.
- See `notebooks/07_evaluation.ipynb` for the reference evaluation walkthrough.

## Reproducibility

- All pipeline stages are deterministic given a fixed `RANDOM_SEED` (see `.env.example`)
  and a pinned dependency set (`requirements.txt`).
- Configuration (region bounds, feature schema, model hyperparameters) lives in
  `config/`, not hardcoded in source, so runs are reproducible from config + code alone.
