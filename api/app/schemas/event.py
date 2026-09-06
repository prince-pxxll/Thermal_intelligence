"""Pydantic response/request schemas for the risk-scoring API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ThermalEvent(BaseModel):
    """A single clustered, risk-scored thermal event."""

    event_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    acq_datetime_ist: datetime
    district: str | None = None
    recurrence_count_30d: int = 0
    persistence_score: float = Field(..., ge=0, le=1)
    anomaly_score: float = Field(..., ge=0, le=1)
    predicted_event_type: str | None = None
    classification_confidence: float | None = Field(default=None, ge=0, le=1)
    risk_score: float = Field(..., ge=0, le=100)
    risk_explanation: str


class EventListResponse(BaseModel):
    """Paginated list of thermal events."""

    total: int
    items: list[ThermalEvent]


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
