# Operations and reproducibility

## Quick local commands

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate ; Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m scripts.run_pipeline
python -m uvicorn backend.app.main:app --reload
```

Browse `http://127.0.0.1:8000/docs` for API endpoints.

Open `frontend/index.html` directly in a browser for the **independent offline simulated dashboard** or run `python -m http.server 8080` from the repository root and open `http://localhost:8080/demo.html`.

## API routes

| Method | Endpoint | Response |
|---|---|---|
| GET | `/api/health` | Demo-mode health |
| GET | `/api/overview` | Aggregates, risks, limitations |
| GET | `/api/forecast/ELEC-101` | Date-indexed forecast, holdout and model selection |
| GET | `/api/inventory/ELEC-101?stock=210` | Replenishment scenario |
| GET | `/api/pricing/ELEC-101?elasticity=-1.4` | Guardrailed pricing sensitivity |

## Reproducible warehouse and BI

After running the pipeline, `data/generated/inventoryiq.db` provides SQL queries/views; `data/generated/bi/` contains five Power BI-ready star-schema CSVs. Both remain local unless you manually publish the **synthetic sample**. Never upload authorized private sales CSVs or imported reports to GitHub Pages.

## Evidence and checks

```bash
python -m unittest discover -s tests -v
python -m scripts.run_pipeline
node --check frontend/app.js
```

`data/generated/report.json` and `data/generated/synthetic_sales.csv` are reproducible output (ignored by Git). These files are generated locally from the fixed seed and are **not** live analytics.

## Security note

The demo has no user login and permits only GET operations. It does not process confidential data. This is not a multi-tenant secured service. Do not expose it as a production stock or price execution API without authentication, rate limits, operational monitoring, audit logging, secure hosting and integration controls.
