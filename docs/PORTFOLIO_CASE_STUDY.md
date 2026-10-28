# InventoryIQ — Predictive Inventory & Dynamic Pricing

**Problem:** Retail inventory planning must balance lost sales risk, holding costs and revenue sensitivity without confusing predictive forecasts with proven pricing outcomes.

**Approach:** Generated 420 days × 8 synthetic SKUs, validated daily price/units and chronological keys, built seasonal-naive and smoothed-weekday forecasts, selected models with expanding-window validation and measured on a sealed 28-day holdout. Converted demand to a reorder point and order-up-to quantity. Added bounded what-if pricing simulations with adjustable assumed elasticity and a 20% minimum modeled gross margin.

**Interface:** Standalone responsive JavaScript dashboard with selectable product, current-stock override, elasticity control, forecasts, safety stock and a scenario comparison table; plus a FastAPI read-only service exposing the Python pipeline.

**Technology:** Python standard library, FastAPI, JavaScript, HTML, CSS, SVG, unittest, GitHub Actions, optional Power BI integration.

**Evidence to show:** Dataset generator, `tests/`, validation folds, model card, exported `data/generated/report.json`, screenshots of the interactive synthetic demo, and the original ten architectural/chart visuals.

**Limitations:** Synthetic records, independent browser mock calculations, no demonstrated live business lift, no trained causal elasticity, no store integration, no public backend deployment or production security certification.

**Recruiter discussion:** Explain why random train-test splits leak temporal information, why holdout must remain unseen during model selection, why a service-level target is not an observed fill rate, and why price changes require experimentation and human review.

## Expanded optional training and BI evidence

A separate [trained RandomForest benchmark](ML_BENCHMARK.md) uses strictly prior-day lag and calendar features, reports a recursive 28-day synthetic holdout, and compares against seasonal naive. The dedicated GitHub Actions run measured 9.328% versus 11.992% WAPE on one synthetic ELEC-101 holdout. Seven Power BI-ready tables now include demand, revenue, stock policies, and **mutually exclusive hypothetical** pricing scenarios; they are not a native Power BI Desktop report. Full [release limitations](RELEASE_READINESS.md) still apply.
