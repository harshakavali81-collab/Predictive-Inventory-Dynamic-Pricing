# Optional trained ML benchmark

The **core** InventoryIQ demonstration deliberately selects two clear, auditable time-series baselines through expanding-fold validation. As an optional trained-machine-learning example, the repository now includes a fixed-hyperparameter scikit-learn `RandomForestRegressor` model using historical daily demand only.

```bash
python -m pip install -r requirements-ml.txt
python -m scripts.run_ml_benchmark --sku ELEC-101 --trees 48
python -m unittest tests.test_ml_benchmark -v
```

Output is generated under `data/generated/ml_benchmark.json`, which is gitignored. The optional GitHub Actions workflow trains/evaluates the same synthetic example and attaches the metrics as an artifact.

## Leakage prevention and evaluation

1. At day `t`, features are computed **exclusively** from the units at previous days: 1, 7, 14 and 28-day lags, rolling means over prior 7 and 28 days, and *known* calendar Fourier features.
2. A fixed-seed random forest is trained only on the 392 days preceding a final 28-day sealed holdout (when using the default 420-day history).
3. The 28-day evaluation forecast is recursive: every new lag comes from a previous **prediction** rather than the unknown holdout actual.
4. The holdout is scored using MAE/WAPE/sMAPE and compared to a seasonal-naive forecast over exactly the same 28-day window. The model has **not** been tuned on holdout metrics.
5. This is a synthetic benchmark, not a validated production model. Feature importance is not a causal explanation. The trained model is optional and does not replace validation-selected baselines in the main application.

No LightGBM, cloud GPU, paid API key or private dataset is needed for this optional training route.
