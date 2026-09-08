"""Create a Day-1 exploratory FRP distribution figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = Path("data/interim/firms_maharashtra_clean.csv")
OUTPUT_PATH = Path("results/figures/day1_frp_distribution.png")


df = pd.read_csv(DATA_PATH)

fig, ax = plt.subplots(figsize=(9, 6))

ax.hist(
    df["frp"],
    bins=8,
    edgecolor="black",
)

ax.axvline(
    df["frp"].median(),
    linestyle="--",
    linewidth=1.5,
    label=f"Median FRP = {df['frp'].median():.2f} MW",
)

ax.set_title(
    "Day-1 EDA: FIRMS Fire Radiative Power Distribution",
    fontsize=14,
    pad=15,
)

ax.set_xlabel("Fire Radiative Power (MW)")
ax.set_ylabel("Number of observations")

ax.grid(
    True,
    linestyle="--",
    linewidth=0.5,
    alpha=0.4,
)

ax.legend()

fig.tight_layout()

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

fig.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print(f"Saved: {OUTPUT_PATH}")
print(f"Observations: {len(df)}")
print(f"Median FRP: {df['frp'].median():.2f} MW")