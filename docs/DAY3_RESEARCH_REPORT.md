# Thermal Intelligence — Day 3 Research Report

## 1. Objective

Day 3 extends the thermal-event pipeline into a geospatially contextualized and explainable anomaly intelligence system for Maharashtra.

## 2. Dataset

- Total feature records: **160**
- Real source-events: **35**
- Synthetic validation events: **125**

## 3. Feature Architecture

- **T — Thermal:** FRP and brightness characteristics
- **τ — Temporal:** activity duration, frequency and day/night behavior
- **S — Spatial:** source footprint and spatial stability
- **G — Geospatial:** industrial, farmland and major-road context

## 4. Geospatial Context

OpenStreetMap context was extracted from the Western Zone regional extract and spatially joined to thermal events.

Derived context features include:
- distance to industrial land use
- distance to farmland
- distance to major roads
- 1 km proximity indicators

## 5. Anomaly Method

Anomaly detection uses robust cohort statistics based only on the 35 real source-events. Median and MAD-based robust z-scores are used to reduce sensitivity to extreme values.

The core anomaly score combines:
- Thermal: 50%
- Temporal: 30%
- Spatial: 20%

## 6. Anomaly Distribution

- normal: **17**
- elevated: **9**
- high: **5**
- extreme: **4**

## 7. Highest-Risk Source-Events

| event_id   |   research_anomaly_score | research_anomaly_level   | anomaly_explanation                                                                                                        |
|:-----------|-------------------------:|:-------------------------|:---------------------------------------------------------------------------------------------------------------------------|
| evt_12     |                 100      | extreme                  | thermal intensity anomaly; spatial footprint anomaly; near industrial land use; near major road                            |
| evt_19     |                  97.1429 | extreme                  | thermal intensity anomaly; temporal activity anomaly; spatial footprint anomaly; near industrial land use; near major road |
| evt_20     |                  94.2857 | extreme                  | temporal activity anomaly; spatial footprint anomaly; near industrial land use                                             |
| evt_21     |                  91.4286 | extreme                  | thermal intensity anomaly; spatial footprint anomaly; near industrial land use; near major road                            |
| evt_8      |                  88.5714 | high                     | thermal intensity anomaly; near industrial land use; near major road                                                       |
| evt_4      |                  85.7143 | high                     | thermal intensity anomaly; spatial footprint anomaly; near industrial land use                                             |
| evt_2      |                  82.8571 | high                     | moderate thermal intensity anomaly                                                                                         |
| evt_11     |                  80      | high                     | temporal activity anomaly; near industrial land use; near major road                                                       |
| evt_7      |                  77.1429 | high                     | moderate thermal intensity anomaly; near industrial land use                                                               |
| evt_14     |                  74.2857 | elevated                 | moderate spatial footprint anomaly                                                                                         |

## 8. Source Profiles

- background-thermal-source: **15**
- industrial-context: **11**
- industrial-like_high-risk: **8**
- elevated-anomaly_unknown-context: **1**

## 9. Controlled Validation

Synthetic perturbations were used only as a stress-test and were excluded from the real-event anomaly baseline. They are not treated as ground-truth labels.

| scenario                |   raw_anomaly_score |   relative_to_baseline |
|:------------------------|--------------------:|-----------------------:|
| baseline                |            0        |               0        |
| high_frp                |            0.773099 |               0.773099 |
| high_brightness         |            0.717039 |               0.717039 |
| high_frequency          |            0.826744 |               0.826744 |
| high_night_activity     |            0        |               0        |
| large_spatial_footprint |            0.600586 |               0.600586 |
| combined_extreme        |            3.4451   |               3.4451   |

## 10. Feature Contribution

- Thermal contribution weight: **50%**
- Temporal contribution weight: **30%**
- Spatial contribution weight: **20%**


Observed mean contributions across real events:
- Thermal: **0.502**
- Temporal: **0.193**
- Spatial: **0.180**


## 11. Scientific Limitations

- The current dataset contains only 35 real source-events and therefore does not support a mature long-term source-specific historical baseline.
- Synthetic events are used for controlled stress testing, not supervised ground truth.
- Industrial proximity represents OSM land-use context, not confirmation of an industrial facility or process.
- Major-road context includes selected major road classes, not the complete road network.
- Settlement context is not yet included.
- Current anomaly weights are expert-designed rather than learned from labeled data.


## 12. Day 3 Conclusion

Day 3 establishes an explainable thermal anomaly intelligence layer combining thermal, temporal, spatial and geospatial context. The system produces ranked source-events with interpretable anomaly drivers and controlled validation evidence.
