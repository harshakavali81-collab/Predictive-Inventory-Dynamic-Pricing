"""Aggregate synthetic KPIs for the demo dashboard."""
from collections import defaultdict

def summarize(rows: list[dict], *, data_source: str = 'synthetic-demo') -> dict:
    sales = sum(row["units"] * row["price"] for row in rows)
    profit = sum(row["units"] * (row["price"] - row["unit_cost"]) for row in rows)
    totals = defaultdict(lambda: {"units": 0, "revenue": 0.0})
    for row in rows:
        rec = totals[row["sku"]]
        rec["units"] += row["units"]
        rec["revenue"] += row["units"] * row["price"]
    return {"records": len(rows), "skus": len(totals), "units": sum(r["units"] for r in rows),
            "revenue": round(sales, 2), "gross_profit": round(profit, 2),
            "by_sku": {sku: {"units": data["units"], "revenue": round(data["revenue"], 2)}
                       for sku, data in sorted(totals.items())}, "data_source": data_source}
