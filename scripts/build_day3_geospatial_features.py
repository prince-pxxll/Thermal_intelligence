from pathlib import Path

import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

FEATURES = ROOT / "data" / "processed" / "feature_table.parquet"
OSM_DIR = ROOT / "data" / "processed" / "osm"

OUT = ROOT / "data" / "processed" / "feature_table_geospatial.parquet"

TARGET_CRS = "EPSG:32643"  # UTM 43N, metres


def load_layer(name):
    path = OSM_DIR / f"{name}.gpkg"
    gdf = gpd.read_file(path)

    print(f"{name}: {len(gdf):,} features")
    print(f"  CRS: {gdf.crs}")
    print(f"  valid: {gdf.geometry.is_valid.mean():.3f}")

    return gdf


def main():

    print("=" * 60)
    print("DAY 3 — GEOSPATIAL FEATURE ENGINEERING")
    print("=" * 60)

    # -------------------------
    # Load thermal features
    # -------------------------
    df = pd.read_parquet(FEATURES)

    print(f"\nThermal rows: {len(df):,}")
    print("Columns:", list(df.columns))

    # Try common coordinate names
    lat_col = next(
        c for c in ["latitude", "lat", "centroid_lat"]
        if c in df.columns
    )

    lon_col = next(
        c for c in ["longitude", "lon", "centroid_lon"]
        if c in df.columns
    )

    thermal = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(
            df[lon_col],
            df[lat_col],
        ),
        crs="EPSG:4326",
    )

    # -------------------------
    # Project to metres
    # -------------------------
    thermal = thermal.to_crs(TARGET_CRS)

    # -------------------------
    # Load OSM layers
    # -------------------------
    industrial = load_layer("industrial")
    farmland = load_layer("farmland")
    roads = load_layer("roads")

    industrial = industrial.to_crs(TARGET_CRS)
    farmland = farmland.to_crs(TARGET_CRS)
    roads = roads.to_crs(TARGET_CRS)

    # -------------------------
    # Nearest industrial
    # -------------------------
    print("\nCalculating distance_to_industry...")

    nearest = gpd.sjoin_nearest(
        thermal,
        industrial[["geometry"]],
        how="left",
        distance_col="distance_to_industry_m",
    )

    nearest = nearest[
        ~nearest.index.duplicated(keep="first")
    ]

    thermal["distance_to_industry_m"] = nearest[
        "distance_to_industry_m"
    ].reindex(thermal.index)

    # -------------------------
    # Nearest road
    # -------------------------
    print("Calculating distance_to_road...")

    nearest = gpd.sjoin_nearest(
        thermal,
        roads[["geometry"]],
        how="left",
        distance_col="distance_to_road_m",
    )

    nearest = nearest[
        ~nearest.index.duplicated(keep="first")
    ]

    thermal["distance_to_road_m"] = nearest[
        "distance_to_road_m"
    ].reindex(thermal.index)

    # -------------------------
    # Nearest farmland
    # -------------------------
    print("Calculating distance_to_farmland...")

    nearest = gpd.sjoin_nearest(
        thermal,
        farmland[["geometry"]],
        how="left",
        distance_col="distance_to_farmland_m",
    )

    nearest = nearest[
        ~nearest.index.duplicated(keep="first")
    ]

    thermal["distance_to_farmland_m"] = nearest[
        "distance_to_farmland_m"
    ].reindex(thermal.index)

    # -------------------------
    # Context flags
    # -------------------------
    thermal["industrial_near_1km"] = (
        thermal["distance_to_industry_m"] <= 1000
    ).astype("int8")

    thermal["road_near_1km"] = (
        thermal["distance_to_road_m"] <= 1000
    ).astype("int8")

    thermal["farmland_near_1km"] = (
        thermal["distance_to_farmland_m"] <= 1000
    ).astype("int8")

    # -------------------------
    # Save
    # -------------------------
    output_df = pd.DataFrame(thermal.drop(columns="geometry"))

    output_df.to_parquet(
        OUT,
        index=False,
    )

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)

    print(f"Saved: {OUT}")
    print(f"Rows: {len(output_df):,}")

    print("\nDistance summary:")
    print(
        output_df[
            [
                "distance_to_industry_m",
                "distance_to_road_m",
                "distance_to_farmland_m",
            ]
        ].describe()
    )


if __name__ == "__main__":
    main()