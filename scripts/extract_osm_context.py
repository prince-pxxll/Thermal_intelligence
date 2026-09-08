from pathlib import Path

import osmium
import geopandas as gpd
from shapely.geometry import LineString, Polygon


ROOT = Path(__file__).resolve().parents[1]

PBF = ROOT / "data" / "raw" / "osm_extract" / "western-zone-latest.osm.pbf"
OUT_DIR = ROOT / "data" / "processed" / "osm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Maharashtra study bounding box
MIN_LON, MIN_LAT = 72.6, 15.6
MAX_LON, MAX_LAT = 80.9, 22.1


def inside_bbox(lon: float, lat: float) -> bool:
    return (
        MIN_LON <= lon <= MAX_LON
        and MIN_LAT <= lat <= MAX_LAT
    )


def way_to_geometry(way):
    coords = []

    for node in way.nodes:
        if not node.location.valid():
            continue

        lon = node.lon
        lat = node.lat

        if inside_bbox(lon, lat):
            coords.append((lon, lat))

    if len(coords) < 2:
        return None

    # Closed way → polygon candidate
    if len(coords) >= 4 and coords[0] == coords[-1]:
        try:
            polygon = Polygon(coords)

            if polygon.is_valid and not polygon.is_empty:
                return polygon
        except Exception:
            pass

    # Otherwise treat as line
    return LineString(coords)


class MaharashtraContextHandler(osmium.SimpleHandler):

    def __init__(self):
        super().__init__()

        self.industrial = []
        self.farmland = []
        self.roads = []
        self.settlements = []

    def way(self, way):

        tags = dict(way.tags)

        # -----------------------------
        # INDUSTRIAL
        # -----------------------------
        if tags.get("landuse") == "industrial":
            geometry = way_to_geometry(way)

            if geometry is not None:
                self.industrial.append(
                    {
                        "osm_id": way.id,
                        "landuse": "industrial",
                        "geometry": geometry,
                    }
                )

        # -----------------------------
        # FARMLAND
        # -----------------------------
        elif tags.get("landuse") == "farmland":
            geometry = way_to_geometry(way)

            if geometry is not None:
                self.farmland.append(
                    {
                        "osm_id": way.id,
                        "landuse": "farmland",
                        "geometry": geometry,
                    }
                )

        # -----------------------------
        # ROADS
        # -----------------------------
        highway = tags.get("highway")

        if highway in {
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
        }:

            geometry = way_to_geometry(way)

            if geometry is not None:
                self.roads.append(
                    {
                        "osm_id": way.id,
                        "highway": highway,
                        "geometry": geometry,
                    }
                )


def save_layer(records, filename):

    if not records:
        print(f"No features found for {filename}")
        return

    gdf = gpd.GeoDataFrame(
        records,
        geometry="geometry",
        crs="EPSG:4326",
    )

    output = OUT_DIR / filename

    gdf.to_file(
        output,
        driver="GPKG",
        layer=filename.replace(".gpkg", ""),
    )

    print(f"Saved: {output}")
    print(f"Features: {len(gdf):,}")


def main():

    if not PBF.exists():
        raise FileNotFoundError(
            f"OSM PBF not found: {PBF}"
        )

    print("=" * 60)
    print("THERMAL INTELLIGENCE — OSM CONTEXT EXTRACTION")
    print("=" * 60)

    print(f"PBF: {PBF}")
    print()
    print("Scanning Western Zone extract...")
    print("Study region: Maharashtra bounding box")
    print()

    handler = MaharashtraContextHandler()

    handler.apply_file(
        str(PBF),
        locations=True,
    )

    print()
    print("Extraction complete.")
    print()

    print(f"Industrial: {len(handler.industrial):,}")
    print(f"Farmland:   {len(handler.farmland):,}")
    print(f"Roads:      {len(handler.roads):,}")

    print()
    print("Writing GeoPackage layers...")
    print()

    save_layer(
        handler.industrial,
        "industrial.gpkg",
    )

    save_layer(
        handler.farmland,
        "farmland.gpkg",
    )

    save_layer(
        handler.roads,
        "roads.gpkg",
    )

    print()
    print("DONE.")


if __name__ == "__main__":
    main()