# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`CHANGELOG.md`](<../CHANGELOG.md>)
- [`Dockerfile`](<../Dockerfile>)
- [`README.md`](<../README.md>)
- [`backend`](<../backend>)
- [`backend/__init__.py`](<../backend/__init__.py>)
- [`backend/app`](<../backend/app>)
- [`backend/app/__init__.py`](<../backend/app/__init__.py>)
- [`backend/app/main.py`](<../backend/app/main.py>)
- [`demo.html`](<../demo.html>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/API_CONTRACT.md`](<../docs/API_CONTRACT.md>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/DATA_DICTIONARY.md`](<../docs/DATA_DICTIONARY.md>)
- [`docs/DEPLOYMENT.md`](<../docs/DEPLOYMENT.md>)
- [`docs/ML_BENCHMARK.md`](<../docs/ML_BENCHMARK.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/PORTFOLIO_CASE_STUDY.md`](<../docs/PORTFOLIO_CASE_STUDY.md>)
- [`docs/RELEASE_READINESS.md`](<../docs/RELEASE_READINESS.md>)
- [`docs/RUNBOOK.md`](<../docs/RUNBOOK.md>)
- [`docs/VERIFIED_RESULTS.md`](<../docs/VERIFIED_RESULTS.md>)
- [`docs/WAREHOUSE.md`](<../docs/WAREHOUSE.md>)
- [`docs/visuals`](<../docs/visuals>)
- [`docs/visuals/01-platform-overview.svg`](<../docs/visuals/01-platform-overview.svg>)
- [`docs/visuals/02-data-pipeline.svg`](<../docs/visuals/02-data-pipeline.svg>)
- [`docs/visuals/03-time-split-evaluation.svg`](<../docs/visuals/03-time-split-evaluation.svg>)
- [`docs/visuals/04-weekly-demand.svg`](<../docs/visuals/04-weekly-demand.svg>)
- [`docs/visuals/05-reorder-policy.svg`](<../docs/visuals/05-reorder-policy.svg>)
- [`docs/visuals/06-pricing-frontier.svg`](<../docs/visuals/06-pricing-frontier.svg>)
- [`docs/visuals/07-elasticity-sensitivity.svg`](<../docs/visuals/07-elasticity-sensitivity.svg>)
- [`docs/visuals/08-assortment-map.svg`](<../docs/visuals/08-assortment-map.svg>)
- [`docs/visuals/09-kpi-map.svg`](<../docs/visuals/09-kpi-map.svg>)
- [`docs/visuals/10-delivery-pipeline.svg`](<../docs/visuals/10-delivery-pipeline.svg>)
- [`frontend`](<../frontend>)
- [`frontend/app.js`](<../frontend/app.js>)
- [`frontend/index.html`](<../frontend/index.html>)
- [`frontend/style.css`](<../frontend/style.css>)
- [`notebooks`](<../notebooks>)
- [`notebooks/01_sales_eda.ipynb`](<../notebooks/01_sales_eda.ipynb>)
- [`notebooks/02_seasonality.ipynb`](<../notebooks/02_seasonality.ipynb>)
- [`notebooks/03_model_comparison.ipynb`](<../notebooks/03_model_comparison.ipynb>)
- [`powerbi`](<../powerbi>)
- [`powerbi/README.md`](<../powerbi/README.md>)
- [`pyproject.toml`](<../pyproject.toml>)
- [`requirements-ml.txt`](<../requirements-ml.txt>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/__init__.py`](<../scripts/__init__.py>)
- [`scripts/check_static_assets.py`](<../scripts/check_static_assets.py>)
- [`scripts/run_ml_benchmark.py`](<../scripts/run_ml_benchmark.py>)
- [`scripts/run_pipeline.py`](<../scripts/run_pipeline.py>)
- [`sql`](<../sql>)
- [`sql/queries.sql`](<../sql/queries.sql>)
- [`sql/schema.sql`](<../sql/schema.sql>)
- [`src`](<../src>)
- [`src/__init__.py`](<../src/__init__.py>)
- [`src/analytics`](<../src/analytics>)
- [`src/analytics/__init__.py`](<../src/analytics/__init__.py>)
- [`src/analytics/bi_exports.py`](<../src/analytics/bi_exports.py>)
- [`src/analytics/report.py`](<../src/analytics/report.py>)
- [`src/analytics/warehouse.py`](<../src/analytics/warehouse.py>)
- [`src/forecasting`](<../src/forecasting>)
- [`src/forecasting/__init__.py`](<../src/forecasting/__init__.py>)
- [`src/forecasting/forecast.py`](<../src/forecasting/forecast.py>)
- [`src/forecasting/ml_benchmark.py`](<../src/forecasting/ml_benchmark.py>)
- [`src/forecasting/uncertainty.py`](<../src/forecasting/uncertainty.py>)
- [`src/ingestion`](<../src/ingestion>)
- [`src/ingestion/__init__.py`](<../src/ingestion/__init__.py>)
- [`src/ingestion/generate.py`](<../src/ingestion/generate.py>)
- [`src/inventory`](<../src/inventory>)
- [`src/inventory/__init__.py`](<../src/inventory/__init__.py>)
- [`src/inventory/position.py`](<../src/inventory/position.py>)
- [`src/inventory/replenishment.py`](<../src/inventory/replenishment.py>)
- [`src/pipeline.py`](<../src/pipeline.py>)
- [`src/pricing`](<../src/pricing>)
- [`src/pricing/__init__.py`](<../src/pricing/__init__.py>)
- [`src/pricing/scenarios.py`](<../src/pricing/scenarios.py>)
- [`src/processing`](<../src/processing>)
- [`src/processing/__init__.py`](<../src/processing/__init__.py>)
- [`src/processing/validation.py`](<../src/processing/validation.py>)
- [`tests`](<../tests>)
- [`tests/test_advanced_planning.py`](<../tests/test_advanced_planning.py>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_bi_exports.py`](<../tests/test_bi_exports.py>)
- [`tests/test_ml_benchmark.py`](<../tests/test_ml_benchmark.py>)
- [`tests/test_pipeline.py`](<../tests/test_pipeline.py>)
- [`tests/test_provenance.py`](<../tests/test_provenance.py>)
- [`tests/test_static_contracts.py`](<../tests/test_static_contracts.py>)
- [`tests/test_warehouse.py`](<../tests/test_warehouse.py>)
