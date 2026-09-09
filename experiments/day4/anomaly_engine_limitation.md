# Day 4 — Anomaly Engine Limitation

The frozen Day-3 anomaly engine uses median/MAD robust z-scores.

For the current 160 source-event dataset, three features have zero global
MAD because of strong concentration at boundary/discrete values:

- detection_frequency_per_day: 130/160 sources at 1.0 (81.25%)
- night_activity_ratio: 83/160 sources at 1.0 (51.88%)
- cluster_radius_km: 125/160 sources at 0.0 (78.12%)

The existing implementation returns a zero contribution when MAD is zero.

Therefore, the frozen Day-3 anomaly output has active anomaly contributions
from max_frp and max_brightness_ti4, while the frequency, night-activity,
and spatial anomaly components are zero for this dataset.

This behavior is retained unchanged for reproducibility.

Day 4 will not overwrite the Day-3 anomaly outputs. Any alternative
zero-MAD treatment will be implemented as a separate experiment and
reported as such.

Status: DOCUMENTED LIMITATION
