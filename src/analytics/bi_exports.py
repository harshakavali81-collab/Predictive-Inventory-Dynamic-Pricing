"""Power BI-ready CSV star-schema exports, fully local and read-only."""
from __future__ import annotations
import csv
from datetime import date, timedelta
from pathlib import Path
from src.ingestion.generate import CATALOG

def _write(path: Path, fields: list[str], records: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer=csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

def export_powerbi_tables(rows: list[dict], report: dict, out: str | Path) -> list[Path]:
    root=Path(out)
    root.mkdir(parents=True,exist_ok=True)
    catalog={p["sku"]:p for p in CATALOG}
    known={p["sku"] for p in report["products"]}
    if known - set(catalog):
        raise ValueError("Cannot export unknown product metadata")
    reported={p["sku"]: p for p in report["products"]}
    products=[{"sku":sku, "product_name":catalog[sku]["name"],"category":catalog[sku]["category"],
               "lead_days":catalog[sku]["lead_days"],"reference_price":reported[sku]["price"],
               "unit_cost":reported[sku]["cost"],"example_on_hand":catalog[sku]["stock"]}
              for sku in sorted(known)]
    dates=sorted(set(r["date"] for r in rows).union(
        d for p in report["products"] for d in p["forecast_dates"]))
    calendar=[{"date":day,"year":date.fromisoformat(day).year,
               "month":date.fromisoformat(day).month,
               "weekday":date.fromisoformat(day).strftime("%A"),
               "week":date.fromisoformat(day).isocalendar().week}
              for day in dates]
    sale_rows=[{"date":r["date"],"sku":r["sku"],"units":r["units"],
                "price":r["price"],"promotion":r["promotion"],"unit_cost":r["unit_cost"],
                "revenue":round(r["price"]*r["units"],2),
                "gross_profit":round((r["price"]-r["unit_cost"])*r["units"],2)}
               for r in rows]
    fcst=[{"date":d,"sku":p["sku"],"forecast_units":p["model"]["future_forecast"][i],
           "model":p["model"]["selected_model"],"data_mode":report["mode"]}
           for p in report["products"] for i,d in enumerate(p["forecast_dates"])]
    scores=[{"sku":p["sku"],"selected_model":p["model"]["selected_model"],
             "holdout_mae":p["model"]["holdout"]["mae"],
             "holdout_wape_pct":p["model"]["holdout"]["wape"],
             "holdout_smape_pct":p["model"]["holdout"]["smape"],
             "baseline_holdout_mae":p["model"]["baseline_holdout"]["mae"],
             "baseline_holdout_wape_pct":p["model"]["baseline_holdout"]["wape"],
             "forecast_start":p["forecast_dates"][0]}
            for p in report["products"]]
    inventories=[{"sku":p["sku"],"current_stock":p["inventory"]["current_stock"],
                  "lead_days":p["inventory"]["lead_time_days"],
                  "safety_stock":p["inventory"]["safety_stock"],
                  "reorder_point":p["inventory"]["reorder_point"],
                  "target_stock":p["inventory"]["target_stock"],
                  "suggested_order":p["inventory"]["order_quantity"],
                  "stock_cover_days":p["inventory"]["stock_cover_days"],
                  "stockout_risk_proxy":p["inventory"]["stockout_risk_proxy"],
                  "data_mode":report["mode"]}
                 for p in report["products"]]
    prices=[{"sku":p["sku"],"change_pct":s["change_pct"],
             "candidate_price":s["price"],"assumed_elasticity":p["pricing"]["assumed_elasticity"],
             "projected_units":s["projected_units"],"projected_revenue":s["projected_revenue"],
             "projected_profit":s["projected_profit"],"gross_margin_pct":s["gross_margin_pct"],
             "recommended_under_assumption":int(s is p["pricing"]["recommended_scenario"]),
             "data_mode":report["mode"]}
            for p in report["products"] for s in p["pricing"]["scenarios"]]
    tables=[
        ("DimProduct.csv",products,["sku","product_name","category","lead_days","reference_price","unit_cost","example_on_hand"]),
        ("DimDate.csv",calendar,["date","year","month","weekday","week"]),
        ("FactSales.csv",sale_rows,["date","sku","units","price","promotion","unit_cost","revenue","gross_profit"]),
        ("FactForecast.csv",fcst,["date","sku","forecast_units","model","data_mode"]),
        ("FactModelQuality.csv",scores,["sku","selected_model","holdout_mae","holdout_wape_pct","holdout_smape_pct","baseline_holdout_mae","baseline_holdout_wape_pct","forecast_start"]),
        ("FactInventory.csv",inventories,["sku","current_stock","lead_days","safety_stock","reorder_point","target_stock","suggested_order","stock_cover_days","stockout_risk_proxy","data_mode"]),
        ("FactPricingScenario.csv",prices,["sku","change_pct","candidate_price","assumed_elasticity","projected_units","projected_revenue","projected_profit","gross_margin_pct","recommended_under_assumption","data_mode"]),
    ]
    result=[]
    for name, data, fields in tables:
        path=root/name
        _write(path,fields,data)
        result.append(path)
    return result
