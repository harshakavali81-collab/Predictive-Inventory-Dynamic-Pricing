# Model card — demand forecast and pricing scenarios

## Purpose and population
Predict next 28 days of units per synthetic SKU, compare safe baselines and illustrate stock decisions. All sales are generated via deterministic code; **no real retailers or customers** are represented.

## Demand models
- `seasonal_naive`: repeat last 7 daily units.
- `weekday_smoothed`: recency-weighted average of up to eight observations of each weekday.
- Four chronological expanding-window validation folds choose the lower MAE model, with tie preference for seasonal naive.
- A final, previously untouched 28-day holdout reports MAE, WAPE and sMAPE. Separate baseline metrics are retained.
- The selected model is fit against all available history only when forecasting the next 28 days.

## Limitations
- No inferred future promotion calendar, no external signals, limited candidate model search.
- Holdout is synthetic, and findings cannot be generalized to a live SKU.
- WAPE is undefined if actual units sum to zero; returns null.
- Uncertainty intervals are not calibrated; volatility-based safety stock is a heuristic.
- Price elasticity (default −1.4) is an adjustable **assumption**, not fitted or validated. Price changes are never automatically applied.

## Decision controls
- Candidate price changes limited to ±10% by default.
- Minimum modeled gross margin 20%.
- Price forecasts and profit results are simulations, not realized ROI.
- Verify costs, availability, law, fairness, experiments and human approvals before any operational use.

## Monitoring / production gaps
Real ingestion, feature drift, bias and promotion sensitivity, uncertainty calibration, backtesting on external real demand, price experiment design, auth, permissions, audit logging and deployment are not included.
