"""Optional trained RandomForest demand benchmark with strictly past-only lag features.

One model is trained on the pre-holdout history. Its recursive 28-day forecast
is scored on the untouched final 28-day synthetic holdout.
It does NOT automatically replace the selection-validated baseline.
"""
from __future__ import annotations
from datetime import date, timedelta
from math import cos, pi, sin
from src.forecasting.forecast import error_metrics, predict

FEATURE_NAMES = ["lag_1", "lag_7", "lag_14", "lag_28", "mean_7", "mean_28",
                 "day_sin", "day_cos", "year_sin", "year_cos"]

def past_features(history: list[float], step: int, start: date) -> list[float]:
    if len(history) != step or step < 28:
        raise ValueError("Expected at least 28 strictly prior daily observations")
    day = start + timedelta(days=step)
    weekday = day.weekday()
    doy = day.timetuple().tm_yday
    return [float(history[-1]),float(history[-7]),float(history[-14]),float(history[-28]),
            sum(history[-7:])/7,sum(history[-28:])/28,
            sin(2*pi*weekday/7),cos(2*pi*weekday/7),
            sin(2*pi*doy/365.25),cos(2*pi*doy/365.25)]

def train_and_evaluate(values: list[int], *, start_date: str = "2025-01-01",
                       horizon: int = 28, n_estimators: int = 48) -> dict:
    try:
        from sklearn.ensemble import RandomForestRegressor
    except ImportError as exc:
        raise RuntimeError("Install optional ML dependencies: pip install -r requirements-ml.txt") from exc
    if not 1 <= horizon <= 90 or len(values) < 120 or len(values) < horizon + 60:
        raise ValueError("Need 120+ observations and at least 60 training days before holdout")
    if not all(type(x) is int and x >= 0 for x in values):
        raise ValueError("Sales units must be nonnegative integers")
    if n_estimators < 16 or n_estimators > 512:
        raise ValueError("n_estimators must be 16..512")
    start = date.fromisoformat(start_date)
    train = values[:-horizon]
    truth = values[-horizon:]
    X = [past_features(train[:i],i,start) for i in range(28,len(train))]
    y = train[28:]
    model = RandomForestRegressor(n_estimators=n_estimators,max_depth=7,min_samples_leaf=3,
                                  random_state=41,n_jobs=1)
    model.fit(X,y)
    history = list(map(float,train))
    predicted = []
    for i in range(horizon):
        estimate = max(0.0,float(model.predict([past_features(history,len(history),start)])[0]))
        predicted.append(round(estimate,2))
        history.append(estimate)
    baseline = predict(train,horizon,"seasonal_naive")
    return {
        "model":"random_forest_recursive", "dataset_mode":"synthetic-demo",
        "training_days":len(train), "holdout_days":horizon,
        "features":FEATURE_NAMES, "n_estimators":n_estimators,
        "holdout":error_metrics(truth,predicted),
        "seasonal_naive_holdout":error_metrics(truth,baseline),
        "actual":truth, "predicted":predicted,
        "feature_importance":{k:round(float(v),4) for k,v in zip(FEATURE_NAMES,model.feature_importances_)},
        "evaluation_note":"Fixed-hyperparameter trained ML baseline. Recursive 28-day holdout only; no claims of real-demand uplift."
    }
