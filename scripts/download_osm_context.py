from pathlib import Path
import json
import time

from thermal_intelligence.config.settings import get_settings
from thermal_intelligence.geospatial.osm import fetch_osm_layer


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "raw" / "osm"
FAILURE_LOG = OUTPUT_DIR / "download_failures.txt"

MIN_LAT = 15.6
MAX_LAT = 22.1
MIN_LON = 72.6
MAX_LON = 80.9

TILE_SIZE = 0.5

# Start with 3 for testing.
# Change to None for the full Maharashtra download.
TEST_TILE_LIMIT = None

LAYERS = {
    "industrial": ["landuse=industrial"],
    "farmland": ["landuse=farmland"],
    "roads": [
        "highway=primary",
        "highway=secondary",
        "highway=tertiary",
    ],
}

MAX_RETRIES = 3
INITIAL_BACKOFF_SECONDS = 5
REQUEST_DELAY_SECONDS = 2


def build_tiles():
    """Build the Maharashtra bounding-box tile grid."""
    tiles = []

    lat = MIN_LAT

    while lat < MAX_LAT:
        lon = MIN_LON
        next_lat = min(lat + TILE_SIZE, MAX_LAT)

        while lon < MAX_LON:
            next_lon = min(lon + TILE_SIZE, MAX_LON)

            tiles.append(
                (
                    round(lat, 6),
                    round(lon, 6),
                    round(next_lat, 6),
                    round(next_lon, 6),
                )
            )

            lon = next_lon

        lat = next_lat

    return tiles


def fetch_with_retry(bbox, tags):
    """Fetch one OSM tile with exponential-backoff retries."""

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fetch_osm_layer(bbox, tags)

        except Exception as exc:
            last_error = exc

            print(
                f"  attempt {attempt}/{MAX_RETRIES} failed: "
                f"{type(exc).__name__}: {exc}"
            )

            if attempt < MAX_RETRIES:
                wait_time = INITIAL_BACKOFF_SECONDS * (2 ** (attempt - 1))

                print(
                    f"  retrying in {wait_time}s..."
                )

                time.sleep(wait_time)

    raise last_error


def log_failure(layer_name, tile_number, bbox, error):
    """Append failed tile information to a persistent log."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(FAILURE_LOG, "a", encoding="utf-8") as f:
        f.write(
            f"{layer_name}\t"
            f"tile={tile_number}\t"
            f"bbox={bbox}\t"
            f"{type(error).__name__}: {error}\n"
        )


def main():
    settings = get_settings()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    tiles = build_tiles()

    if TEST_TILE_LIMIT is None:
        selected_tiles = tiles
    else:
        selected_tiles = tiles[:TEST_TILE_LIMIT]

    print("OSM context downloader")
    print("Overpass:", settings.overpass_api_url)
    print("Total tiles:", len(tiles))
    print("Tiles selected:", len(selected_tiles))
    print("Layers:", ", ".join(LAYERS))
    print()

    for layer_name, tags in LAYERS.items():

        layer_dir = OUTPUT_DIR / layer_name
        layer_dir.mkdir(parents=True, exist_ok=True)

        for i, bbox in enumerate(selected_tiles, start=1):

            output = layer_dir / f"tile_{i:03d}.json"

            if output.exists():
                print(
                    f"[{layer_name}] "
                    f"tile {i}/{len(tiles)} already exists"
                )
                continue

            print(
                f"[{layer_name}] "
                f"tile {i}/{len(tiles)} "
                f"bbox={bbox}"
            )

            try:
                data = fetch_with_retry(bbox, tags)

                with open(output, "w", encoding="utf-8") as f:
                    json.dump(data, f)

                elements = len(data.get("elements", []))

                print(
                    f"  saved: {elements} elements"
                )

            except Exception as exc:

                print(
                    f"  FAILED permanently: "
                    f"{type(exc).__name__}: {exc}"
                )

                log_failure(
                    layer_name,
                    i,
                    bbox,
                    exc,
                )

            time.sleep(REQUEST_DELAY_SECONDS)


if __name__ == "__main__":
    main()