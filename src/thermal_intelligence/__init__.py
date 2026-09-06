"""Thermal Intelligence — Maharashtra.

A geospatial pipeline for ingesting, clustering, contextualizing, and risk-scoring
satellite-derived thermal anomalies over Maharashtra.

Subpackages
-----------
config       Typed settings loader (env + YAML).
data         Ingestion, validation, and preprocessing of raw thermal-anomaly data.
geospatial   Spatiotemporal clustering, distance calculations, OSM context joins.
features     Thermal, temporal, persistence, and contextual feature builders.
models       Classification, anomaly detection, and evaluation.
risk         Risk scoring and human-readable explanation generation.
pipelines    End-to-end orchestration scripts tying the above together.
"""

__version__ = "0.1.0"
