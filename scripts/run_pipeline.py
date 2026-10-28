"""Generate synthetic dataset, metrics and standalone frontend artifact."""
import json
from pathlib import Path
from src.ingestion.generate import generate_sales, save_csv
from src.pipeline import build_report

def main():
    sales = generate_sales()
    report = build_report(sales)
    save_csv(sales, "data/generated/synthetic_sales.csv")
    for path in ("data/generated/report.json", "frontend/report.json"):
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Generated", len(sales), "synthetic transactions for", len(report["products"]), "products")
    for item in report["products"]:
        print(item["sku"], item["model"]["selected_model"], "holdout WAPE=", item["model"]["holdout"]["wape"])

if __name__ == "__main__":
    main()
