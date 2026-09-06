# Contributing

Thanks for considering a contribution to Thermal Intelligence — Maharashtra.

## Ground rules

- Be respectful and constructive — see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- Every change should be traceable: a PR should map to an issue, an ADR, or a clear
  one-line rationale in the description.
- Don't commit data. `data/`, `models/`, and `results/` are git-ignored except for
  `.gitkeep` placeholders and small reference fixtures under `tests/fixtures/`.

## Development setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
pre-commit install   # if configured locally
```

## Workflow

1. **Fork/branch** — branch from `main` using `feat/<short-desc>`, `fix/<short-desc>`,
   or `docs/<short-desc>`.
2. **Write tests first where practical** — unit tests under `tests/unit/`, integration
   tests under `tests/integration/`.
3. **Run the full check locally** before opening a PR:
   ```bash
   make lint
   make test
   ```
4. **Keep PRs focused.** One logical change per PR. Large refactors should be discussed
   in an issue first.
5. **Update docs.** If you change data schemas, config, or pipeline behavior, update the
   relevant file under `docs/` in the same PR.
6. **Architecture decisions.** Non-trivial design choices (new dependency, schema change,
   modeling approach change) should get a short ADR in `docs/decisions/`.

## Code style

- Python ≥ 3.10, formatted with `black`, linted with `ruff`, type-checked with `mypy`
  where feasible (see `pyproject.toml`).
- Docstrings: Google style.
- Prefer pure functions in `src/thermal_intelligence/*` modules; keep I/O and
  orchestration in `pipelines/`.

## Commit messages

Conventional Commits style is preferred:

```
feat(geospatial): add DBSCAN-based spatiotemporal clustering
fix(data): correct FIRMS confidence field parsing
docs(methodology): clarify persistence scoring window
```

## Reporting bugs / requesting features

Open a GitHub issue with:
- What you expected vs. what happened
- Minimal reproduction steps (or a failing test)
- Environment details (OS, Python version)

## Security issues

Do **not** open a public issue. See [`SECURITY.md`](SECURITY.md).
