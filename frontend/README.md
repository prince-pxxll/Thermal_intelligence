# Frontend (placeholder)

No frontend client has been built yet. This directory is reserved for a future
visualization client — e.g. a map-based dashboard showing clustered thermal events,
risk scores, and explanations, consuming the API defined in `api/app/`.

## Intended shape (not yet implemented)

- A map view (e.g. Leaflet/Mapbox) plotting events from `GET /events`, colored by
  `risk_score`.
- A detail panel showing `risk_explanation` and contributing feature values for a
  selected event.
- District-level filtering and time-range selection.

## Suggested stack (open to change via an ADR in `docs/decisions/`)

- Vite + React + TypeScript
- A mapping library (MapLibre GL or Leaflet — prefer MapLibre for open-source tile
  compatibility)
- Fetches directly from the FastAPI service in `api/app/` (see `main.py`)

## Getting started (once scaffolded)

```bash
cd frontend
npm install
npm run dev
```

Until this is built out, use the API directly (`make api`, then visit `/docs` for
the interactive OpenAPI UI) or the notebooks in `notebooks/` for exploratory
visualization.
