"""NASA FIRMS ingestion client.

Wraps the FIRMS API (area/CSV endpoints) for pulling active-fire detections over a
bounding box and date range. See docs/data_sources.md for field definitions and
docs/methodology.md for how this fits into the wider pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd
import requests

from thermal_intelligence.config.settings import get_settings

FIRMS_EXPECTED_COLUMNS = [
    "latitude",
    "longitude",
    "brightness",
    "scan",
    "track",
    "acq_date",
    "acq_time",
    "satellite",
    "confidence",
    "version",
    "bright_t31",
    "frp",
    "daynight",
]


@dataclass(frozen=True)
class FirmsQuery:
    """Parameters for a single FIRMS ingestion request."""

    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    start_date: date
    end_date: date
    instrument: str = "VIIRS_SNPP_NRT"


def build_area_url(query: FirmsQuery) -> str:
    """Construct the FIRMS area-API URL for the given query.

    TODO: confirm exact endpoint path/date-window semantics against the current
    FIRMS API docs before first live run (the API accepts a `day_range` rather than
    arbitrary start/end in some versions).
    """
    settings = get_settings()
    bbox = f"{query.min_lon},{query.min_lat},{query.max_lon},{query.max_lat}"
    day_range = (query.end_date - query.start_date).days + 1
    return (
        f"{settings.firms_base_url}/area/csv/{settings.firms_map_key}/"
        f"{query.instrument}/{bbox}/{day_range}/{query.start_date.isoformat()}"
    )


def fetch_detections(query: FirmsQuery, timeout_s: int = 60) -> pd.DataFrame:
    """Fetch raw FIRMS detections for `query` and return them as a DataFrame.

    Raises `requests.HTTPError` on a non-2xx response. Does not filter or clean the
    result — see `thermal_intelligence.data.preprocessing` for that.
    """
    url = build_area_url(query)
    response = requests.get(url, timeout=timeout_s)
    response.raise_for_status()

    from io import StringIO

    df = pd.read_csv(StringIO(response.text))
    missing = set(FIRMS_EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"FIRMS response missing expected columns: {sorted(missing)}")
    return df


def save_raw(df: pd.DataFrame, out_dir: Path, query: FirmsQuery) -> Path:
    """Persist a raw, unmodified FIRMS pull to `data/raw/firms/`.

    File naming encodes the query window so raw pulls remain traceable to their
    retrieval parameters (see docs/data_sources.md, "data provenance discipline").
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = (
        f"firms_{query.instrument}_{query.start_date.isoformat()}_"
        f"{query.end_date.isoformat()}.csv"
    )
    out_path = out_dir / filename
    df.to_csv(out_path, index=False)
    return out_path
