"""OpenStreetMap extraction and spatial join utilities.

Pulls land-use, industrial-zone, and road-network layers via the Overpass API (or a
pre-downloaded `.pbf`/`.gpkg` extract) and joins them against clustered thermal events
for contextual feature construction.
"""

from __future__ import annotations

import geopandas as gpd
import requests

from thermal_intelligence.config.settings import get_settings

OVERPASS_TIMEOUT_S = 180


def build_overpass_query(bbox: tuple[float, float, float, float], tags: list[str]) -> str:
    """Build an Overpass QL query for the given bounding box and OSM tag filters.

    `bbox` is (min_lat, min_lon, max_lat, max_lon). `tags` are Overpass tag filters,
    e.g. `["landuse=industrial", "landuse=farmland"]`.
    """
    min_lat, min_lon, max_lat, max_lon = bbox
    bbox_str = f"{min_lat},{min_lon},{max_lat},{max_lon}"
    clauses = "\n".join(f'  way["{t.split("=")[0]}"="{t.split("=")[1]}"]({bbox_str});' for t in tags)
    return f"""
[out:json][timeout:{OVERPASS_TIMEOUT_S}];
(
{clauses}
);
out body geom;
""".strip()


def fetch_osm_layer(bbox: tuple[float, float, float, float], tags: list[str]) -> dict:
    """Fetch raw Overpass JSON for the given bbox/tags. Caller is responsible for
    converting the response into a GeoDataFrame (e.g. via `osm2geojson` or manual
    parsing) before persisting to `data/raw/osm/`.
    """
    settings = get_settings()
    query = build_overpass_query(bbox, tags)
    response = requests.post(settings.overpass_api_url, data={"data": query}, timeout=OVERPASS_TIMEOUT_S)
    response.raise_for_status()
    return response.json()


def load_landuse_layer(path: str) -> gpd.GeoDataFrame:
    """Load a previously-saved land-use layer (GeoJSON/GPKG/Shapefile) from disk."""
    return gpd.read_file(path)
