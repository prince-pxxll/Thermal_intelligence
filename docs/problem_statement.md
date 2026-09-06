# Problem Statement

## Context

Maharashtra experiences a high volume of satellite-detected thermal anomalies each year,
driven by a mix of agricultural residue burning, industrial thermal emissions, wildfires,
gas flaring, and sporadic false positives (e.g. sun glint, solar panel reflection). Raw
thermal-anomaly feeds — such as NASA FIRMS active-fire detections — report *where heat was
detected*, not *what caused it* or *how much it matters*.

This creates a gap for anyone who needs to act on thermal signals: environmental
regulators tracking illegal burning, disaster-response teams monitoring wildfire risk,
insurers assessing industrial fire exposure, or researchers studying land-use change.

## The problem

> Raw thermal-anomaly detections are noisy, decontextualized, and non-differentiated.
> There is no readily available layer that clusters, contextualizes, and risk-scores
> these detections at the granularity needed for operational decision-making in
> Maharashtra specifically.

Concretely:

1. **Volume & noise** — thousands of detections per season, many redundant, some
   spurious.
2. **No persistence signal** — a single-day hotspot and a hotspot recurring for two weeks
   look identical in raw feeds, but imply very different risk.
3. **No spatial context** — a thermal anomaly near a factory, near cropland, and inside a
   forest reserve carry different implications, but raw feeds don't encode proximity to
   infrastructure or land use.
4. **No explainability** — flagging something as "high risk" without a reason is not
   actionable for downstream users (regulators, responders) who need to justify action.

## Why this project

This project builds an end-to-end pipeline — from raw ingestion to an explainable risk
score — specifically scoped to Maharashtra, to make thermal-anomaly data usable rather
than merely available.

See [`research_question.md`](research_question.md) for the specific questions this
project answers, and [`methodology.md`](methodology.md) for the analytical approach.
