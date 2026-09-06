"""FastAPI application entry point.

Run locally with:
    uvicorn api.app.main:app --reload

or via:
    make api
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.app.routes import events, health
from thermal_intelligence import __version__
from thermal_intelligence.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="Thermal Intelligence — Maharashtra API",
    description="Serves clustered, risk-scored thermal-anomaly events for Maharashtra.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(events.router)


@app.get("/")
def root() -> dict:
    return {
        "name": "Thermal Intelligence — Maharashtra API",
        "version": __version__,
        "docs": "/docs",
    }
