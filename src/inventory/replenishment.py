"""Periodic-review reorder advice using illustrative lead-time and stock assumptions."""
import math
from statistics import pstdev, mean

SERVICE_Z = {0.90: 1.282, 0.95: 1.645, 0.98: 2.054, 0.99: 2.326}

def recommend(forecast: list[float], historical_units: list[int], on_hand: int,
              lead_days: int, review_days: int = 7, service_level: float = 0.95) -> dict:
    if not forecast or len(historical_units) < 14:
        raise ValueError("Missing demand information")
    if type(on_hand) is not int or on_hand < 0 or type(lead_days) is not int or not 1 <= lead_days <= 60:
        raise ValueError("Invalid stock or lead time")
    if type(review_days) is not int or not 1 <= review_days <= 30 or service_level not in SERVICE_Z:
        raise ValueError("Unsupported review period or service level")
    daily = mean(forecast)
    # Volatility is a proxy based on recent raw sales; not a forecast-error-calibrated service model.
    variability = pstdev(historical_units[-56:])
    safety = math.ceil(SERVICE_Z[service_level] * variability * math.sqrt(lead_days))
    reorder_point = math.ceil(daily * lead_days + safety)
    target = math.ceil(daily * (lead_days + review_days) + safety)
    suggested = max(0, target - on_hand) if on_hand <= reorder_point else 0
    cover = on_hand / daily if daily > 0 else None
    return {
        "daily_demand": round(daily, 2), "demand_std_proxy": round(variability, 2),
        "safety_stock": safety, "reorder_point": reorder_point, "target_stock": target,
        "current_stock": on_hand, "order_quantity": suggested,
        "stock_cover_days": round(cover, 2) if cover is not None else None,
        "stockout_risk_proxy": "high" if cover is not None and cover < lead_days else "moderate" if on_hand <= reorder_point else "low",
        "service_level_target": service_level, "lead_time_days": lead_days, "review_days": review_days,
        "note": "Planning heuristic; requires calibrated demand variance, lead-time uncertainty and live stock for operations."
    }
