"""Typed application settings.

Settings are loaded from environment variables (via `.env`, see `.env.example`) and
merged with `config/project.yaml`. Use `get_settings()` everywhere rather than reading
`os.environ` or YAML directly, so there is a single source of truth and it stays
mockable in tests.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROJECT_CONFIG = PROJECT_ROOT / "config" / "project.yaml"


class Settings(BaseSettings):
    """Runtime settings sourced from environment variables.

    See `.env.example` at the repository root for the full list of supported
    variables and their defaults.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    firms_map_key: str = Field(default="", alias="FIRMS_MAP_KEY")
    firms_base_url: str = Field(
        default="https://firms.modaps.eosdis.nasa.gov/api", alias="FIRMS_BASE_URL"
    )

    copernicus_client_id: str = Field(default="", alias="COPERNICUS_CLIENT_ID")
    copernicus_client_secret: str = Field(default="", alias="COPERNICUS_CLIENT_SECRET")

    overpass_api_url: str = Field(
        default="https://overpass-api.de/api/interpreter", alias="OVERPASS_API_URL"
    )

    region_config_path: Path = Field(
        default=PROJECT_ROOT / "config" / "regions" / "maharashtra.yaml",
        alias="REGION_CONFIG_PATH",
    )

    data_root: Path = Field(default=PROJECT_ROOT / "data", alias="DATA_ROOT")
    models_root: Path = Field(default=PROJECT_ROOT / "models", alias="MODELS_ROOT")
    results_root: Path = Field(default=PROJECT_ROOT / "results", alias="RESULTS_ROOT")

    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_log_level: str = Field(default="info", alias="API_LOG_LEVEL")

    random_seed: int = Field(default=42, alias="RANDOM_SEED")
    environment: str = Field(default="development", alias="ENVIRONMENT")


def load_project_config(path: Path = DEFAULT_PROJECT_CONFIG) -> dict[str, Any]:
    """Load `config/project.yaml` (pipeline parameters, not secrets)."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached `Settings` instance.

    Cached because settings are immutable for the lifetime of a process; tests that
    need fresh settings should call `get_settings.cache_clear()` first.
    """
    return Settings()
