"""OpenStreetMap extraction and spatial-context utilities."""

from __future__ import annotations

import geopandas as gpd
import requests
from shapely.geometry import LineString, Polygon

from thermal_intelligence.config.settings import get_settings


OVERPASS_TIMEOUT_S = 180


def build_overpass_query(
    bbox: tuple[float, float, float, float],
    tags: list[str],
) -> str:
    """Build an Overpass query for OSM way features.

    bbox = (min_lat, min_lon, max_lat, max_lon)
    """

    min_lat, min_lon, max_lat, max_lon = bbox
    bbox_str = f"{min_lat},{min_lon},{max_lat},{max_lon}"

    clauses = "\n".join(
        f'  way["{tag.split("=")[0]}"]'
        f'["{tag.split("=")[0]}"="{tag.split("=")[1]}"]'
        f"({bbox_str});"
        for tag in tags
    )

    return f"""
[out:json][timeout:{OVERPASS_TIMEOUT_S}];
(
{clauses}
);
out body geom;
""".strip()


def fetch_osm_layer(
    bbox: tuple[float, float, float, float],
    tags: list[str],
) -> dict:
    """Fetch raw OSM way geometry from Overpass."""

    settings = get_settings()

    query = build_overpass_query(bbox, tags)

    headers = {
        "User-Agent": "ThermalIntelligence/0.1 (research project)",
        "Referer": "https://www.openstreetmap.org/",
    }

    response = requests.post(
        settings.overpass_api_url,
        data={"data": query},
        headers=headers,
        timeout=OVERPASS_TIMEOUT_S,
    )

    response.raise_for_status()

    return response.json()


def osm_json_to_geodataframe(data: dict) -> gpd.GeoDataFrame:
    """Convert Overpass way geometries to a GeoDataFrame.

    Closed ways with >= 4 coordinates are represented as polygons.
    Open ways are represented as LineStrings.
    """

    records = []

    for element in data.get("elements", []):
        if element.get("type") != "way":
            continue

        geometry = element.get("geometry", [])

        if len(geometry) < 2:
            continue

        coordinates = [
            (point["lon"], point["lat"])
            for point in geometry
        ]

        is_closed = coordinates[0] == coordinates[-1]

        if is_closed and len(coordinates) >= 4:
            geom = Polygon(coordinates)
        else:
            geom = LineString(coordinates)

        tags = element.get("tags", {})

        row = {
            "osm_id": element.get("id"),
            "osm_type": element.get("type"),
            "geometry": geom,
        }

        for key, value in tags.items():
            row[f"tag_{key}"] = value

        records.append(row)

    if not records:
        return gpd.GeoDataFrame(
            columns=["osm_id", "osm_type", "geometry"],
            geometry="geometry",
            crs="EPSG:4326",
        )

    return gpd.GeoDataFrame(
        records,
        geometry="geometry",
        crs="EPSG:4326",
    )


def load_landuse_layer(path: str) -> gpd.GeoDataFrame:
    """Load a previously-saved OSM/vector layer."""

    return gpd.read_file(path)