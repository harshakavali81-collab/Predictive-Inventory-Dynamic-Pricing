"""Descriptive nonnegative error bands from past expanding-fold residuals.

These are not statistically guaranteed conformal prediction intervals because
the same validation folds also select the model. Treat bands as heuristic.
"""
from __future__ import annotations
from math import ceil, isfinite

def residual_band(residuals: list[float], estimates: list[float], target: float = 0.90) -> dict:
    if not residuals or not estimates or not 0.5 < target < 1:
        raise ValueError("Need residuals, estimates and a target between 0.5 and 1")
    if any((not isfinite(x)) or x < 0 for x in residuals):
        raise ValueError("Residuals must be finite and nonnegative")
    if any((not isfinite(x)) or x < 0 for x in estimates):
        raise ValueError("Forecasts must be finite and nonnegative")
    ordered = sorted(residuals)
    index = min(len(ordered)-1, max(0,ceil((len(ordered)+1)*target)-1))
    width = ordered[index]
    return {
        "nominal_target":target, "calibration_observations":len(residuals),
        "absolute_error_width":round(width,2),
        "lower":[round(max(0,x-width),2) for x in estimates],
        "upper":[round(x+width,2) for x in estimates],
        "method":"validation residual absolute-error band (descriptive; not a guaranteed prediction interval)"
    }

def observed_coverage(actual: list[int], lower: list[float], upper: list[float]) -> float:
    if not actual or len(actual)!=len(lower) or len(actual)!=len(upper):
        raise ValueError("Unmatched or missing coverage inputs")
    return round(sum(lo <= a <= hi for a,lo,hi in zip(actual,lower,upper))/len(actual),3)
