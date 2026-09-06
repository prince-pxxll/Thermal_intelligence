"""Event query endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from api.app.schemas.event import EventListResponse, ThermalEvent
from api.app.services import event_service

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=EventListResponse)
def list_events(
    min_risk_score: float | None = Query(default=None, ge=0, le=100),
    district: str | None = Query(default=None),
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
) -> EventListResponse:
    """List risk-scored thermal events, optionally filtered by risk score / district."""
    total, page = event_service.get_events(
        min_risk_score=min_risk_score, district=district, limit=limit, offset=offset
    )
    items = [ThermalEvent(**row) for row in page.to_dict(orient="records")]
    return EventListResponse(total=total, items=items)


@router.get("/{event_id}", response_model=ThermalEvent)
def get_event(event_id: str) -> ThermalEvent:
    """Fetch a single event by ID."""
    row = event_service.get_event_by_id(event_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Event '{event_id}' not found")
    return ThermalEvent(**row.to_dict())
