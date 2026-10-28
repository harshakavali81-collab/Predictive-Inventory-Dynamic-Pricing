"""Illustrative elasticity-driven scenarios; no causal elasticity is estimated."""
def simulate(base_price: float, unit_cost: float, forecast_units: float, elasticity: float = -1.4,
             max_change: float = 0.10, min_margin: float = 0.20) -> dict:
    if not 0 < unit_cost < base_price or forecast_units < 0:
        raise ValueError("Invalid economic inputs")
    if not -4 <= elasticity <= -0.1 or not 0 < max_change <= 0.20 or not 0 <= min_margin < 0.8:
        raise ValueError("Scenario constraints violated")
    baseline_profit = (base_price - unit_cost) * forecast_units
    scenarios = []
    for step in (-0.10, -0.05, 0.0, 0.05, 0.10):
        if abs(step) > max_change + 1e-9:
            continue
        candidate = round(base_price * (1 + step), 2)
        margin = (candidate - unit_cost) / candidate
        if margin + 1e-9 < min_margin:
            continue
        quantity = forecast_units * (candidate / base_price) ** elasticity
        revenue = quantity * candidate
        profit = quantity * (candidate - unit_cost)
        scenarios.append({
            "change_pct": round(step * 100), "price": candidate,
            "projected_units": round(quantity, 2), "projected_revenue": round(revenue, 2),
            "projected_profit": round(profit, 2), "gross_margin_pct": round(100 * margin, 2),
            "profit_change_pct": round(100 * (profit / baseline_profit - 1), 2) if baseline_profit else 0.0
        })
    if not scenarios:
        raise ValueError("No prices satisfy guardrails")
    best = max(scenarios, key=lambda s: (s["projected_profit"], -abs(s["change_pct"])))
    return {
        "assumed_elasticity": elasticity, "max_change_pct": round(max_change * 100),
        "min_margin_pct": round(min_margin * 100), "recommended_scenario": best,
        "scenarios": scenarios,
        "warning": "Hypothetical simulation only. Elasticity is an assumption, not identified from observational sales; never auto-apply prices."
    }
