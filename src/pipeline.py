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

def build_report(rows: list[dict] | None = None, *, source_label: str = "synthetic-demo") -> dict:
    if source_label not in ("synthetic-demo", "imported-local-csv"):
        raise ValueError("Unsupported data source label")
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
        # CSV imports use their latest observed price/cost, not the example catalog prices.
        # Example stock and lead times remain configured assumptions, not ERP snapshots.
        ref_price = item["price"] if source_label == "synthetic-demo" else float(history[-1]["price"])
        ref_cost = item["cost"] if source_label == "synthetic-demo" else float(history[-1]["unit_cost"])
        inventory = recommend(model["future_forecast"], [r["units"] for r in history], item["stock"], item["lead_days"])
        pricing = simulate(ref_price, ref_cost, sum(model["future_forecast"]))
        products.append({
            "sku": sku, "name": item["name"], "category": item["category"],
            "price": ref_price, "cost": ref_cost,
            "reference_price_source": "sample_catalog" if source_label == "synthetic-demo" else "most_recent_observation",
            "inventory_metadata_source": "illustrative_catalog_assumptions",
            "history": history[-70:],
            "model": model, "inventory": inventory, "pricing": pricing,
            "forecast_dates": [(latest_day + timedelta(days=i + 1)).isoformat() for i in range(28)]
        })
    return {"project": "InventoryIQ", "mode": source_label,
            "generated_from": "fixed-seed synthetic sales" if source_label == "synthetic-demo" else "user-supplied local CSV (unverified)",
            "as_of": latest_day.isoformat(), "overview": summarize(validated, data_source=source_label), "products": products,
            "limitations": [
                "No valid real-world demand performance is established by these results.",
                "Pricing elasticity is assumed; no causal evaluation or real-world price optimization.",
                "Stock and lead times are sample settings, not integrated ERP inventory.",
                "Holdout metrics are out-of-sample for the chosen validation-selected model, not external validation.",
                "Observed sales may be censored by stockouts; promotions and returns require additional handling."
            ]}
