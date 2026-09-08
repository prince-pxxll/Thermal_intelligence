from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

BASE = ROOT / "data" / "processed" / "feature_table.parquet"
GEO = ROOT / "data" / "processed" / "feature_table_geospatial.parquet"

OUT = ROOT / "data" / "processed" / "feature_table.parquet"


def main():

    base = pd.read_parquet(BASE)
    geo = pd.read_parquet(GEO)

    geo_cols = [
        "event_id",
        "distance_to_industry_m",
        "distance_to_road_m",
        "distance_to_farmland_m",
        "industrial_near_1km",
        "road_near_1km",
        "farmland_near_1km",
    ]

    geo = geo[geo_cols]

    # Remove old geospatial columns if this script is rerun.
    drop_cols = [
        c for c in geo_cols
        if c != "event_id" and c in base.columns
    ]

    base = base.drop(columns=drop_cols)

    merged = base.merge(
        geo,
        on="event_id",
        how="left",
        validate="one_to_one",
    )

    merged.to_parquet(
        OUT,
        index=False,
    )

    print("=" * 60)
    print("DAY 3 — CANONICAL FEATURE TABLE UPDATED")
    print("=" * 60)

    print(f"Rows:    {len(merged):,}")
    print(f"Columns: {len(merged.columns):,}")

    print("\nGeospatial features:")
    for col in geo_cols[1:]:
        print(
            f"{col}: "
            f"{merged[col].notna().sum():,}/{len(merged):,}"
        )

    print(f"\nSaved: {OUT}")


if __name__ == "__main__":
    main()