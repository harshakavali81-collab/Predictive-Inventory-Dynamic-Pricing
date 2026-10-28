# InventoryIQ — release readiness evidence and blockers

## Implemented and verified with GitHub Actions

- Reproducible 420-day × 8-SKU generated sales pipeline, 3,360 daily product observations.
- Sales schema validation, local CSV import safeguards, deterministic reports and provenance tags.
- Expanding-window time-series model selection, sealed 28-day holdout, baseline metrics and descriptive forecast-error bands.
- Inventory-position scenarios, safety-stock heuristics, allocations and backorders, order caps and case-pack rounding.
- Assumption-based elasticity pricing with ±10% candidate changes and modeled ≥20% gross-margin guardrails. *No live price changes.*
- FastAPI read-only forecasting, inventory and pricing endpoints.
- SQLite warehouse and five Power BI-ready CSV star-schema tables.
- Browser dashboard, ten original SVG diagrams, three notebook examples and technical documentation.
- CI builds a non-root Docker image and exercises the local API health endpoint.

## Deployment requirements

GitHub Pages on the dedicated repository requires owner activation. A workflow **succeeds when it safely skips deployment due to missing Pages configuration**; that is not evidence that the website has been deployed. Follow [deployment instructions](DEPLOYMENT.md), then confirm both the Pages deployment run and real site URL.

Portfolio repository contains a standalone independent browser demo and project study. The portfolio may experience rate-limited deployment runs even if its static code passed tests. The client-side demo falls back to clearly labeled independent illustrative calculations when the Python `report.json` asset is absent.

## Not completed or not verified

- A verified, publicly hosted FastAPI backend with secure multi-user identity management.
- Real point-of-sale/ERP data ingestion, stock ledger reconciliation and stockout censored-demand adjustments.
- A causal or randomized price-elasticity estimate, real profit uplift, verified fill rate or reliable demand-interval coverage on real retail data.
- A native edited Power BI Desktop `.pbix` report (the source provides import-ready CSVs and DAX instructions).
- Production threat modelling, audited authentication/authorization, monitoring alerts, alert delivery, scheduled renewals, backups and disaster recovery.
- Real merchant consent, policy sign-off and operational deployment. **Do not auto-execute stock or pricing actions.**

## Operational go/no-go checklist

- [ ] Confirm authorization for all real data sources and document PII/sensitive-data review.
- [ ] Validate missing date and censored-demand policies for actual SKU histories.
- [ ] Run time-sliced benchmarks on external, real historical demand, with segment-level diagnostics.
- [ ] Calibrate interval coverage and simulate lost-sales/holding-cost scenarios with real prices and lead times.
- [ ] Obtain experimentation and price fairness/compliance review.
- [ ] Deploy authenticated API in approved infrastructure with controlled secrets and audit logs.
- [ ] Run integration/roll-back tests against an approved sandbox merchant system.
- [ ] Activate GitHub Pages or equivalent static hosting and independently verify live URL.
- [ ] Build and inspect a native Power BI report if that deliverable is required.
- [ ] Obtain stakeholder sign-off before any business decisions are automated.
