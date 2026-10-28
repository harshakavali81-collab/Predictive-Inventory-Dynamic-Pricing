# Verified synthetic-pipeline results

An expanded CI run on October 28, 2026 also passed **29 tests** and verified the SQLite warehouse plus five Power BI-ready export tables. [View the expanded successful workflow](https://github.com/harshakavali81-collab/Predictive-Inventory-Dynamic-Pricing/actions/runs/40656569570). The earlier per-SKU WAPE metrics below are from the identical deterministic synthetic generator.


**Evidence:** [GitHub Actions run #1](https://github.com/harshakavali81-collab/Predictive-Inventory-Dynamic-Pricing/actions/runs/40654347916), 2026-10-28. The CI job concluded **success**, executed **18 Python/API tests**, generated 3,360 synthetic daily product observations and checked JavaScript syntax.

## Last-28-day holdout results

The pipeline chooses between two baseline methods using four chronological validation folds *before* scoring the sealed 28-day holdout.

| SKU | Selected method | Holdout WAPE |
|---|---|---:|
| ELEC-101 | weekday_smoothed | 10.006% |
| ELEC-102 | weekday_smoothed | 13.240% |
| HOME-201 | weekday_smoothed | 14.183% |
| HOME-202 | seasonal_naive | 20.296% |
| LIFE-301 | weekday_smoothed | 10.097% |
| LIFE-302 | weekday_smoothed | 13.158% |
| OFFC-401 | weekday_smoothed | 13.595% |
| OFFC-402 | weekday_smoothed | 10.413% |

These results are **algorithmic measurements on synthetic generated data**. They do not establish accuracy on real-world demand. WAPE should not be averaged across SKUs without considering the weighting definition. Reproduce or inspect the other MAE, sMAPE and baseline fields through `python -m scripts.run_pipeline` and the generated `data/generated/report.json`.

No real revenue improvement, inventory cost savings, filled orders, true realized stockout prevention, or deployed production performance was measured.

## Optional trained ML result — synthetic only

The optional RandomForest recursive benchmark passed three dedicated unit tests in [GitHub Actions](https://github.com/harshakavali81-collab/Predictive-Inventory-Dynamic-Pricing/actions/runs/40659428133). For the **ELEC-101 28-day synthetic holdout only**, RandomForest WAPE = **9.328%**, seasonal-naive WAPE = **11.992%**. The result was obtained with fixed hyperparameters and strict historical lag features; it cannot be extrapolated to other products or real stores. The trained model is intentionally separate from the main application model-selection process.
