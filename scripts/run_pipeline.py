"""Generate the demo or process an explicitly supplied, authorized CSV locally.

--input never writes reports into web-served frontend/ by default.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from collections import defaultdict
from datetime import date, timedelta
from src.ingestion.generate import generate_sales, save_csv, read_csv
from src.pipeline import build_report
from src.processing.validation import validate_sales
from src.analytics.warehouse import export_warehouse

def validate_continuous_daily_history(rows: list[dict]) -> None:
    grouped = defaultdict(list)
    for item in rows:
        grouped[item["sku"]].append(date.fromisoformat(item["date"]))
    for sku, dates in grouped.items():
        ordered = sorted(dates)
        if len(ordered) < 120:
            raise ValueError(f"{sku}: needs at least 120 daily observations")
        if len(ordered) != (ordered[-1] - ordered[0]).days + 1:
            raise ValueError(f"{sku}: missing daily dates; zero-sales days must be explicit")
    if len(rows) > 100_000:
        raise ValueError("Limit: 100,000 observations")

def main(args=None):
    parser = argparse.ArgumentParser(description="Build demo forecast and local SQLite/JSON reports")
    parser.add_argument("--input", type=Path, help="Authorized local CSV (strict configured SKU schema)")
    parser.add_argument("--output", type=Path, default=Path("data/generated/report.json"))
    parser.add_argument("--sqlite", type=Path, default=Path("data/generated/inventoryiq.db"))
    options = parser.parse_args(args)
    if options.input:
        if options.input.stat().st_size > 10_000_000:
            raise ValueError("CSV input exceeds 10 MB local limit")
        sales = read_csv(options.input)
        source = "imported-local-csv"
        if options.output.resolve().is_relative_to(Path("frontend").resolve()):
            raise ValueError("Do not write imported data or reports into the public frontend directory")
    else:
        sales = generate_sales()
        source = "synthetic-demo"
        save_csv(sales, "data/generated/synthetic_sales.csv")
    sales = validate_sales(sales)
    validate_continuous_daily_history(sales)
    report = build_report(sales, source_label=source)
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    db = export_warehouse(sales, options.sqlite)
    if not options.input:
        target = Path("frontend/report.json")
        target.write_text(json.dumps(report, separators=(",", ":")), encoding="utf-8")
    print("Mode:", source, "Rows:", len(sales), "Products:", len(report["products"]), "Warehouse:", db)
    for product in report["products"]:
        print(product["sku"], product["model"]["selected_model"],
              "holdout WAPE=", product["model"]["holdout"]["wape"])

if __name__ == "__main__":
    main()
