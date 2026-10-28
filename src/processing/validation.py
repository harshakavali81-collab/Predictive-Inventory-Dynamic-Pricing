"""Fail-closed validation of sale records and time keys."""
from datetime import date

REQUIRED = {"date", "sku", "category", "units", "price", "promotion", "unit_cost"}

def validate_sales(rows: list[dict]) -> list[dict]:
    if not rows:
        raise ValueError("Sales dataset is empty")
    keys = set()
    for i, row in enumerate(rows):
        if not REQUIRED.issubset(row):
            raise ValueError(f"Record {i}: missing required fields")
        try:
            date.fromisoformat(str(row["date"]))
        except ValueError as exc:
            raise ValueError(f"Record {i}: invalid ISO date") from exc
        key = (row["date"], row["sku"])
        if key in keys:
            raise ValueError(f"Duplicate date/SKU key: {key}")
        keys.add(key)
        if not str(row["sku"]).strip() or not str(row["category"]).strip():
            raise ValueError(f"Record {i}: missing SKU or category")
        if type(row["units"]) is not int or row["units"] < 0:
            raise ValueError(f"Record {i}: units must be a nonnegative integer")
        if not 0 < float(row["unit_cost"]) < float(row["price"]):
            raise ValueError(f"Record {i}: unit cost must be positive and below price")
        if row["promotion"] not in (0, 1):
            raise ValueError(f"Record {i}: promotion must be 0 or 1")
    return sorted(rows, key=lambda row: (row["sku"], row["date"]))
