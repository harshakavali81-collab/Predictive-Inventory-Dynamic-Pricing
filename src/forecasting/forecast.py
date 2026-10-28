"""Seasonal naive vs smoothed weekday forecasting with chronological backtests.

Training never reads evaluation targets. Holdout is untouched during model choice.
"""
from __future__ import annotations
import math
from statistics import mean

def predict(history: list[int], horizon: int, model: str) -> list[float]:
    if len(history) < 14 or horizon < 1 or horizon > 90:
        raise ValueError("Need 14+ historical points and a horizon in 1..90")
    if model not in ("seasonal_naive", "weekday_smoothed"):
        raise ValueError("Unknown forecasting model")
    week = history[-7:]
    if model == "seasonal_naive":
        return [float(max(0, week[i % 7])) for i in range(horizon)]
    # Last 8 occurrences of each weekday, weighted toward recent observations.
    result = []
    for i in range(horizon):
        weekday_position = i % 7
        offsets = list(range(len(history) - 7 + weekday_position, -1, -7))[:8]
        values = [history[pos] for pos in offsets]
        weights = list(range(len(values), 0, -1))
        estimate = sum(v * w for v, w in zip(values, weights)) / sum(weights)
        result.append(round(max(0.0, estimate), 2))
    return result

def error_metrics(y_true: list[int], y_pred: list[float]) -> dict:
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("Mismatched or empty evaluation arrays")
    mae = mean(abs(a - p) for a, p in zip(y_true, y_pred))
    denominator = sum(abs(a) for a in y_true)
    wape = 100 * sum(abs(a - p) for a, p in zip(y_true, y_pred)) / denominator if denominator else None
    smape = mean(200 * abs(a - p) / (abs(a) + abs(p)) if a or p else 0 for a, p in zip(y_true, y_pred))
    return {"mae": round(mae, 3), "wape": round(wape, 3) if wape is not None else None, "smape": round(smape, 3)}

def backtest(values: list[int], horizon: int = 28, folds: int = 4, window: int = 14) -> dict:
    if len(values) < horizon + folds * window + 28:
        raise ValueError("Not enough history for chronological validation and test")
    trainval, holdout = values[:-horizon], values[-horizon:]
    errors = {"seasonal_naive": [], "weekday_smoothed": []}
    for fold in range(folds):
        end = len(trainval) - (folds - fold - 1) * window
        hist = trainval[:end - window]
        truth = trainval[end - window:end]
        for model in errors:
            errors[model].append(error_metrics(truth, predict(hist, window, model))["mae"])
    mean_mae = {model: round(mean(vals), 3) for model, vals in errors.items()}
    selected = min(mean_mae, key=lambda model: (mean_mae[model], model != "seasonal_naive"))
    test_pred = predict(trainval, horizon, selected)
    baseline_pred = predict(trainval, horizon, "seasonal_naive")
    future = predict(values, horizon, selected)
    return {
        "selected_model": selected, "validation_folds": folds, "validation_mae": mean_mae,
        "holdout_days": horizon, "holdout": error_metrics(holdout, test_pred),
        "baseline_holdout": error_metrics(holdout, baseline_pred),
        "holdout_actual": holdout, "holdout_predicted": test_pred,
        "future_forecast": [round(v, 2) for v in future]
    }
