# Test Fixtures

Small, static reference datasets used by unit/integration tests. These are checked
into git (unlike `data/`) specifically because they're tiny, synthetic-or-scrubbed,
and needed for tests to run offline and deterministically.

- `sample_firms_detections.csv` — a 4-row FIRMS-shaped sample used to validate
  schema checks, preprocessing, and clustering without hitting the live API.
