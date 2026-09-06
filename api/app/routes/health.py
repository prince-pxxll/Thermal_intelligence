"""Liveness/readiness endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from api.app.schemas.event import HealthResponse
from thermal_intelligence import __version__

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)
