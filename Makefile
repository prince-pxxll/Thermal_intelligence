.PHONY: help install install-dev lint format type-check test test-unit test-integration \
        ingest preprocess features train evaluate pipeline api clean

PYTHON ?= python
PIP ?= pip

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: ## Install dev + runtime dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

lint: ## Run ruff lint checks
	ruff check src tests scripts api

format: ## Auto-format code with black + ruff
	black src tests scripts api
	ruff check --fix src tests scripts api

type-check: ## Run mypy static type checking
	mypy src

test: test-unit test-integration ## Run all tests

test-unit: ## Run unit tests
	pytest tests/unit -v

test-integration: ## Run integration tests
	pytest tests/integration -v

ingest: ## Run the data ingestion pipeline
	$(PYTHON) -m thermal_intelligence.pipelines.ingest

preprocess: ## Run preprocessing on ingested data
	$(PYTHON) -m thermal_intelligence.pipelines.preprocess

build-sources: ## Build joined/derived source datasets (FIRMS + OSM + Sentinel)
	$(PYTHON) -m thermal_intelligence.pipelines.build_sources

features: build-sources ## Build model-ready feature tables
	$(PYTHON) -m thermal_intelligence.pipelines.build_features

train: ## Train models
	$(PYTHON) -m thermal_intelligence.pipelines.train

evaluate: ## Evaluate trained models
	$(PYTHON) -m thermal_intelligence.pipelines.evaluate

pipeline: ingest preprocess features train evaluate ## Run the full end-to-end pipeline

api: ## Run the FastAPI service locally
	uvicorn api.app.main:app --reload --host 0.0.0.0 --port 8000

clean: ## Remove caches and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
