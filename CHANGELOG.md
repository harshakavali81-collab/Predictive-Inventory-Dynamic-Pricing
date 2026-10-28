# InventoryIQ Changelog

## 1.2.0 — 2026-10-28

- Reproducible synthetic 28-day retail forecasting, sealed holdout and baseline comparison.
- Descriptive validation-residual demand uncertainty bands and observed holdout coverage (not guaranteed confidence intervals).
- Extended inventory-position scenarios: on-order units, allocations, backorders, case packs and capped orders.
- Guardrailed assumption-based pricing simulations with read-only API.
- FastAPI local dashboard hosting, SQLite analytical schema, five Power BI-ready exports.
- Independent accessible static dashboard with product/stock/elasticity controls and optional Python report consumption.
- Fixed-seed dataset, ten original SVG illustrations, three notebooks and documented business limitations.
- CI Python/API/warehouse/static tests, JavaScript syntax, local Docker health smoke test.
- Pages build workflow and deployment readiness checklist; public site activation not automatically assumed.

This project is a synthetic-data educational demonstration. No production retail metrics or real price changes are claimed.

## 1.3.0 — 2026-10-28

- Added trained, recursive, strictly past-only Random Forest demand benchmark with dedicated scikit-learn test workflow.
- Expanded BI exports to seven CSV tables, including stock and constrained price-scenario facts; scenario totals must not double-count mutually exclusive alternatives.
- Verified 46 core tests and Docker health smoke test, plus three dedicated ML benchmark tests, before these documentation updates.
