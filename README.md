# InventoryIQ — Predictive Inventory & Dynamic Pricing

**An end-to-end, reproducible synthetic retail intelligence portfolio project.** Forecast SKU demand, evaluate models chronologically, calculate reorder quantities and explore constrained pricing scenarios through FastAPI and an interactive browser dashboard.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![InventoryIQ platform](<docs/visuals/01-platform-overview.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Existing published preview link: [Open browser preview](https://harshakavali81-collab.github.io/Predictive-Inventory-Dynamic-Pricing/demo.html`). This update does not independently verify its availability or backend deployment.

## Key Features

- Fixed-seed, repeatable daily sales history for eight products across four categories.
- Input schema validation and duplicate-date/SKU rejection.
- Seasonal naïve and weighted-weekday demand forecasting, four expanding-window validation folds, untouched final 28-day test, MAE/WAPE/sMAPE reporting.
- Forecast-driven lead-time demand, safety stock, reorder point, target stock, recommended quantity and indicative stock-cover risk.
- Assumption-based price scenario simulations (−10/−5/0/+5/+10%), 20% gross margin floor and manual-only candidate review.
- Read-only FastAPI with bounded query parameters and local CORS restrictions.
- Responsive, dependency-free static dashboard with editable product, on-hand units and elasticity sliders.
- Tests, CI configuration, architecture/model/data documentation and ten original vector figures.

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/Predictive-Inventory-Dynamic-Pricing.git
cd Predictive-Inventory-Dynamic-Pricing
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m scripts.run_pipeline
uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API. For the standalone frontend, open `frontend/index.html` directly or run `python -m http.server 8080` at the repo root and open `http://localhost:8080/demo.html`.

Generated outputs: `data/generated/synthetic_sales.csv`, `data/generated/report.json` and `frontend/report.json`. These are ignored from version control and can be recreated by the runner.

## Challenges & Solutions

`src/forecasting/forecast.py` selects the lower-MAE forecast on four growing-window folds and then reports selected-model and seasonal-baseline errors on the untouched final 28-day test. WAPE is undefined when the actual holdout total is zero; that value is returned as `null`, rather than fabricated. Once evaluated, it forecasts 28 future days using the complete history.

Stock decisions are heuristics based on a fixed 95% service target and historical sales variation. Reorder point = lead-time forecast demand + illustrative safety stock. Order quantity = maximum of zero and target stock minus on-hand, **only if on-hand is at or below reorder point**.

Pricing explores a constant-elasticity relation to reference forecast units. Projected gross profit is before shipping, taxes, fixed costs and returns. The "best" candidate is only best under the chosen assumptions. No prices are changed or sent to an external service.

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

**An end-to-end, reproducible synthetic retail intelligence portfolio project.** Forecast SKU demand, evaluate models chronologically, calculate reorder quantities and explore constrained pricing scenarios through FastAPI and an interactive browser dashboard.



> **Demo notice:** The dataset, stock, prices and forecast performance are all synthetic or simulated. Pricing elasticity is an assumption, not a causally estimated effect. The dashboard is an independent illustrative browser demo, not a live backend deployment.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `sql/` | SQL schema and analysis |
| `powerbi/` | Power BI build assets |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Predictive-Inventory-Dynamic-Pricing/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

