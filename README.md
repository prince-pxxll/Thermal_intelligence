# Thermal Intelligence — Maharashtra

Satellite-derived thermal anomaly intelligence for Maharashtra: ingestion, spatiotemporal
clustering, feature engineering, and risk scoring built on NASA FIRMS active-fire data,
Sentinel imagery, and OpenStreetMap context layers.

## What this is

A research and engineering pipeline that turns raw thermal-anomaly detections into
explainable, geolocated risk signals — e.g. distinguishing agricultural burning from
industrial thermal events, flagging persistent hotspots, and surfacing anomalies against
land-use and infrastructure context.

## Project layout

```
thermal-intelligence-maharashtra/
├── docs/            problem framing, methodology, data sources, assumptions, limitations
├── config/          project & region configuration (YAML)
├── data/            raw / interim / processed / labels / external (git-ignored contents)
├── notebooks/       exploration -> modeling -> evaluation, in numbered order
├── src/thermal_intelligence/   installable Python package (see below)
├── tests/           unit + integration tests, shared fixtures
├── experiments/     baselines, ablations, model configs, run logs
├── results/         figures, tables, metrics, generated reports
├── models/          checkpoints and packaged model artifacts
├── api/             FastAPI service exposing scoring endpoints
├── frontend/        (placeholder) client for visualizing risk output
└── scripts/         thin CLI entry points around the pipelines
```

### `src/thermal_intelligence/` package

| Module | Responsibility |
|---|---|
| `config/` | Typed settings loader (env + YAML) |
| `data/` | FIRMS ingestion, schema validation, preprocessing |
| `geospatial/` | Spatiotemporal clustering, distance calcs, OSM joins, spatial features |
| `features/` | Thermal, temporal, persistence, and contextual feature builders |
| `models/` | Classification, anomaly detection, evaluation metrics |
| `risk/` | Risk scoring and human-readable explanation generation |
| `pipelines/` | End-to-end orchestration: ingest → preprocess → features → train → evaluate |

## Quickstart

```bash
# 1. Clone and enter
git clone <repo-url> && cd thermal-intelligence-maharashtra

# 2. Create environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# 3. Configure secrets
cp .env.example .env   # fill in FIRMS_MAP_KEY, etc.

# 4. Run the pipeline
make ingest
make features
make train
make evaluate
```

Or step through `notebooks/00_data_exploration.ipynb` onward for an interactive walkthrough.

## Documentation

- [`docs/problem_statement.md`](docs/problem_statement.md) — why this project exists
- [`docs/research_question.md`](docs/research_question.md) — what we're trying to answer
- [`docs/methodology.md`](docs/methodology.md) — the analytical approach
- [`docs/data_sources.md`](docs/data_sources.md) — inputs and provenance
- [`docs/assumptions.md`](docs/assumptions.md) — working assumptions
- [`docs/limitations.md`](docs/limitations.md) — known limitations and caveats
- [`docs/decisions/`](docs/decisions/README.md) — architecture decision records (ADRs)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Security

See [`SECURITY.md`](SECURITY.md) for how to report vulnerabilities.

## License

MIT — see [`LICENSE`](LICENSE).

## Citation

If you use this work, please cite via [`CITATION.cff`](CITATION.cff).
