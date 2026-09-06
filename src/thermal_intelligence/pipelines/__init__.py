"""End-to-end orchestration scripts: ingest -> preprocess -> features -> train -> evaluate.

Each module here is runnable as `python -m thermal_intelligence.pipelines.<stage>` and
also exposes a `main()` function for programmatic invocation (e.g. from the Makefile
or an orchestrator like Airflow/Prefect in the future).
"""
