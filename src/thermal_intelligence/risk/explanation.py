"""Human-readable rationale generation for risk scores.

Turns the numeric components behind `scoring.compute_risk_score` into a short
natural-language explanation, so downstream users (regulators, responders) get a
reason alongside a number. See docs/limitations.md — "risk scores are decision
support, not enforcement determinations."
"""

from __future__ import annotations

import pandas as pd


def _risk_tier(score: float) -> str:
    if score >= 70:
        return "High"
    if score >= 40:
        return "Moderate"
    return "Low"


def explain_event(row: pd.Series) -> str:
    """Build a one-line explanation for a single event's risk score.

    Expects `row` to contain: risk_score, recurrence_count_30d, dist_to_industrial_m,
    predicted_event_type (optional), anomaly_score.
    """
    tier = _risk_tier(row["risk_score"])
    parts = [f"{tier} risk ({row['risk_score']:.0f}/100):"]

    recurrence = row.get("recurrence_count_30d")
    if pd.notna(recurrence) and recurrence >= 3:
        parts.append(f"recurring detection ({int(recurrence)}x in 30 days)")
    else:
        parts.append("isolated detection")

    dist_industrial = row.get("dist_to_industrial_m")
    if pd.notna(dist_industrial) and dist_industrial < 1000:
        parts.append(f"{dist_industrial:.0f}m from an industrial zone")

    anomaly = row.get("anomaly_score")
    if pd.notna(anomaly) and anomaly > 0:
        parts.append("flagged as anomalous relative to seasonal baseline")

    event_type = row.get("predicted_event_type")
    if pd.notna(event_type):
        parts.append(f"classified as likely {event_type}")

    return ", ".join(parts) + "."


def add_explanations(feature_table: pd.DataFrame) -> pd.DataFrame:
    """Add a `risk_explanation` column to `feature_table` in place-safe fashion."""
    out = feature_table.copy()
    out["risk_explanation"] = out.apply(explain_event, axis=1)
    return out
