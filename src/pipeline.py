"""Orchestrated retail planning report. Read-only what-if recommendations."""
from __future__ import annotations
from collections import defaultdict
from datetime import date, timedelta
from src.ingestion.generate import CATALOG, generate_sales
from src.processing.validation import validate_sales
from src.forecasting.forecast import backtest
from src.inventory.replenishment import recommend
from src.pricing.scenarios import simulate
from src.analytics.report import summarize

def build_report(rows: list[dict] | None = None) -> dict:
    validated = validate_sales(generate_sales() if rows is None else rows)
    grouped = defaultdict(list)
    for row in validated:
        grouped[row["sku"]].append(row)
    catalog_by_sku = {p["sku"]: p for p in CATALOG}
    products = []
    latest_day = date.fromisoformat(max(r["date"] for r in validated))
    for sku, history in sorted(grouped.items()):
        if sku not in catalog_by_sku:
            raise ValueError(f"Unknown SKU: {sku}; configure catalog metadata before planning")
        item = catalog_by_sku[sku]
        model = backtest([r["units"] for r in history])
        inventory = recommend(model["future_forecast"], [r["units"] for r in history], item["stock"], item["lead_days"])
        pricing = simulate(item["price"], item["cost"], sum(model["future_forecast"]))
        products.append({
            "sku": sku, "name": item["name"], "category": item["category"],
            "price": item["price"], "cost": item["cost"], "history": history[-70:],
            "model": model, "inventory": inventory, "pricing": pricing,
            "forecast_dates": [(latest_day + timedelta(days=i + 1)).isoformat() for i in range(28)]
        })
    return {"project": "InventoryIQ", "mode": "synthetic-demo", "generated_from": "fixed-seed synthetic sales",
            "as_of": latest_day.isoformat(), "overview": summarize(validated), "products": products,
            "limitations": [
                "Synthetic transactions, not real demand or commercial performance.",
                "Pricing elasticity is assumed; no causal evaluation or real-world price optimization.",
                "Stock and lead times are sample settings, not integrated ERP inventory.",
                "Holdout metrics are out-of-sample for the chosen validation-selected model, not external validation."
            ]}
