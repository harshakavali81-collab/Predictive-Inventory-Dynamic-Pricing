# InventoryIQ Deployment and operational boundaries

## Public static GitHub Pages demo

The `.github/workflows/pages.yml` workflow tests and generates a **fixed-seed synthetic** report in GitHub Actions, then uploads the site (browser code, diagrams and report.json) to Pages. The browser loads that JSON and surfaces actual **Python-model holdout evaluation**, while scenario adjustments remain browser-side what-ifs.

**Owner setup:** On the project repository, open **Settings → Pages → Build and deployment → Source: GitHub Actions**. GitHub Pages may need to be enabled by the repository owner. Once workflow deployment succeeds, visit:

`https://harshakavali81-collab.github.io/Predictive-Inventory-Dynamic-Pricing/demo.html`

Do not claim that URL works unless the Pages deployment has succeeded and the page has been opened successfully.

## Local Docker demo

```bash
docker compose up --build -d
docker compose ps
```

Open `http://127.0.0.1:8000/demo/` for the dashboard and `http://127.0.0.1:8000/docs` for OpenAPI. The container serves the bundled generated *synthetic* report and a read-only API.

This compose binds to **localhost only**, runs as an unprivileged container user, has read-only filesystem and disallows gaining new privileges. It does not implement real user authentication or external integration; never expose the port to an untrusted network.

## Imported CSV mode (local only)

```bash
python -m scripts.run_pipeline --input /path/to/authorized_sales.csv --output data/generated/local_report.json --sqlite data/generated/local.sqlite
```

Use only data you are authorized to process. Import checks required schema, date/SKU uniqueness and complete daily histories for each configured SKU. It **never** publishes imported records into `frontend/report.json`. Imported rows are saved only where specified locally. The catalog continues to use example costs, stock and lead-time metadata—do not treat imported reports as operational decisions.

## What is NOT deployed

- No always-on FastAPI cloud service or production login/multi-tenant authorization.
- No actual POS/ERP stock adjustments or price changes.
- No validated live demand uplift or causal elasticity.
- No private-data pipeline for public GitHub Pages.
- No native Power BI Desktop file.

Production release would require authorized stores, time-stamped inventory snapshots, stockout censored-demand handling, experiments, calibration, secrets management, backup/restore, audit logs, IAM, domain security review, real-world monitoring and stakeholder approval.

## Hostable static build even if Pages is not activated

The Pages workflow produces an `inventoryiq-static-site` artifact using `actions/upload-artifact`. Download it from the run details to deploy the synthetic-only frontend with the same folder structure to any static host. A passing **build/artifact** step is not proof of a public Pages deployment.
