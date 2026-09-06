# Experiments

Tracked experiment configs, ablations, and run logs — separate from `results/`
(generated outputs) and `models/` (final trained artifacts).

## Layout

- **`baselines/`** — reference configs and results for the simplest reasonable
  approach to each problem (e.g. majority-class classifier, fixed-threshold
  confidence filter with no clustering). Every new modeling approach should beat its
  baseline before being adopted, and the comparison should be recorded here.
- **`ablations/`** — systematic removal/variation of one component at a time (e.g.
  "clustering without temporal dimension", "risk score without context_severity
  weight") to understand each component's contribution.
- **`models/`** — configuration files (hyperparameters, feature sets) for each model
  variant tried, named descriptively, e.g. `gbc_v1_no_context.yaml`.
- **`runs/`** — timestamped run logs/metrics snapshots (git-ignored by default — see
  `.gitignore` — since these can grow large; promote a run's summary into
  `results/reports/` if it should be preserved long-term).

## Convention

Each experiment config should record enough to reproduce the run:

```yaml
name: gbc_v2_with_persistence
date: 2026-09-06
base_config: config/project.yaml
overrides:
  modeling.classification.algorithm: gradient_boosting
  clustering.spatial_eps_km: 0.75
notes: >
  Adds persistence_score as a classifier feature; compare against
  baselines/gbc_v1_no_persistence for lift.
```

Record the outcome (metrics, a link to the `results/` artifact) in the same file or
a matching `*_results.md` once the run completes.
