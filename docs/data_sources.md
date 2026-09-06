# Data Sources

## Primary: NASA FIRMS (Fire Information for Resource Management System)

- **What**: Active-fire / thermal-anomaly detections derived from MODIS (Terra/Aqua) and
  VIIRS (Suomi NPP, NOAA-20/21) instruments.
- **Fields used**: latitude, longitude, brightness/bright_ti4, scan, track, acquisition
  date/time, satellite, confidence, version, bright_ti5, FRP (fire radiative power),
  daynight.
- **Access**: FIRMS API (`FIRMS_MAP_KEY` required — see `.env.example`), bounded to the
  Maharashtra region as defined in `config/regions/maharashtra.yaml`.
- **Resolution**: ~375m (VIIRS) / ~1km (MODIS) per detection pixel.
- **License / usage**: Public domain (NASA); attribution requested. See NASA FIRMS
  citation guidance for report/publication use.
- **Stored at**: `data/raw/firms/` (raw, immutable).

## Secondary: OpenStreetMap (OSM)

- **What**: Land-use polygons, industrial zone boundaries, road/rail infrastructure,
  administrative boundaries for Maharashtra.
- **Access**: Overpass API (`OVERPASS_API_URL`) or a regional `.pbf` extract.
- **License**: Open Database License (ODbL) — attribution required, share-alike for
  derived data extracts.
- **Stored at**: `data/raw/osm/`.

## Secondary: Sentinel (Copernicus)

- **What**: Sentinel-2 (optical, 10m) and Sentinel-3 (SLSTR thermal, ~1km) imagery used
  for visual confirmation of clustered events and, optionally, additional thermal
  cross-referencing.
- **Access**: Copernicus Data Space Ecosystem API (`COPERNICUS_CLIENT_ID` /
  `COPERNICUS_CLIENT_SECRET`).
- **License**: Copernicus open data license — free, attribution required.
- **Stored at**: `data/raw/sentinel/`.

## Other / supplementary (`data/raw/other/`)

Placeholder for ad hoc supplementary sources as needed, for example:
- District/administrative boundary shapefiles (e.g. from Survey of India / GADM, subject
  to their respective licenses — verify before redistribution).
- Historical fire-incident records for label construction (`data/labels/`), where
  available from state pollution control board or forest department disclosures.

## Data provenance discipline

- Raw data (`data/raw/`) is never modified in place — all cleaning happens on read into
  `data/interim/` and `data/processed/`.
- Every ingestion run should record: source, query parameters (date range, bounding
  box), retrieval timestamp, and API/data version, so that downstream results are
  traceable back to a specific pull. See `pipelines/ingest.py`.
- Large raw/processed data files are **not** committed to git (see `.gitignore`); use
  DVC, a cloud bucket, or documented manual retrieval steps for reproducing datasets.
