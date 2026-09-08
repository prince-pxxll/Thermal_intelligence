"""Create the Day-1 QA map for cleaned FIRMS observations."""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
DATA_PATH = Path("data/interim/firms_maharashtra_clean.csv")
BOUNDARY_PATH = Path(
    "data/external/maharashtra_boundary/MAHARASHTRA_STATE_BDY.shp"
)
OUTPUT_PATH = Path("results/figures/day1_firms_thermal_observations.png")


# ---------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

boundary = gpd.read_file(BOUNDARY_PATH).to_crs("EPSG:4326")

points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df["longitude"],
        df["latitude"],
    ),
    crs="EPSG:4326",
)


# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 10))

# Maharashtra boundary
boundary.boundary.plot(
    ax=ax,
    linewidth=1.2,
)

# FIRMS observations
points.plot(
    ax=ax,
    markersize=35,
    alpha=0.85,
)

# Labels
ax.set_title(
    "Day-1 QA Map: FIRMS Thermal Anomaly Observations\n"
    f"Maharashtra | {len(points)} cleaned observations",
    fontsize=14,
    pad=15,
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Scientific map appearance
ax.grid(
    True,
    linestyle="--",
    linewidth=0.5,
    alpha=0.4,
)

ax.set_aspect("equal")

# Keep geographic extent tied to Maharashtra
minx, miny, maxx, maxy = boundary.total_bounds
padding_x = (maxx - minx) * 0.03
padding_y = (maxy - miny) * 0.03

ax.set_xlim(minx - padding_x, maxx + padding_x)
ax.set_ylim(miny - padding_y, maxy + padding_y)


# ---------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

fig.tight_layout()
fig.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print(f"Saved: {OUTPUT_PATH}")
print(f"Observations plotted: {len(points)}")
print(f"CRS: {points.crs}")