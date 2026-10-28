"""Deterministic, synthetic sales data. Never represents actual business transactions."""
from __future__ import annotations
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

CATALOG = [
    {"sku": "ELEC-101", "name": "Wireless Headphones", "category": "Electronics", "base_demand": 32, "price": 2199, "cost": 1200, "lead_days": 10, "stock": 210},
    {"sku": "ELEC-102", "name": "Bluetooth Speaker", "category": "Electronics", "base_demand": 24, "price": 3499, "cost": 2050, "lead_days": 12, "stock": 110},
    {"sku": "HOME-201", "name": "Desk Lamp", "category": "Home", "base_demand": 27, "price": 1299, "cost": 620, "lead_days": 7, "stock": 240},
    {"sku": "HOME-202", "name": "Storage Organizer", "category": "Home", "base_demand": 39, "price": 899, "cost": 400, "lead_days": 5, "stock": 290},
    {"sku": "LIFE-301", "name": "Reusable Bottle", "category": "Lifestyle", "base_demand": 45, "price": 749, "cost": 320, "lead_days": 6, "stock": 350},
    {"sku": "LIFE-302", "name": "Yoga Mat", "category": "Lifestyle", "base_demand": 20, "price": 1599, "cost": 680, "lead_days": 9, "stock": 160},
    {"sku": "OFFC-401", "name": "Notebook Pack", "category": "Office", "base_demand": 50, "price": 599, "cost": 250, "lead_days": 4, "stock": 460},
    {"sku": "OFFC-402", "name": "Ergonomic Stand", "category": "Office", "base_demand": 17, "price": 2699, "cost": 1250, "lead_days": 11, "stock": 90},
]

def generate_sales(days: int = 420, seed: int = 41) -> list[dict]:
    if days < 120:
        raise ValueError("At least 120 days required for time-aware evaluation")
    rng = random.Random(seed)
    start = date(2025, 1, 1)
    rows = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        weekend = day.weekday() >= 5
        season = 1 + 0.16 * math.sin(2 * math.pi * offset / 365)
        month_boost = 1.20 if day.month in (10, 11, 12) else 1
        for index, product in enumerate(CATALOG):
            promo = int(((offset + index * 13) % 47) < 6)
            promotion_factor = 1.24 if promo else 1.0
            weekday_factor = (1.18 if weekend else 1.0) * (0.92 if day.weekday() == 0 else 1.0)
            noise = max(0.5, rng.gauss(1.0, 0.12))
            units = max(0, round(product["base_demand"] * season * month_boost * promotion_factor * weekday_factor * noise))
            price = round(product["price"] * (0.92 if promo else 1.0), 2)
            rows.append({
                "date": day.isoformat(), "sku": product["sku"], "category": product["category"],
                "units": units, "price": price, "promotion": promo,
                "unit_cost": product["cost"]
            })
    return rows

def save_csv(rows: list[dict], output: str | Path) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No rows to export")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path

def read_csv(path: str | Path) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["units"] = int(row["units"])
        row["price"] = float(row["price"])
        row["unit_cost"] = float(row["unit_cost"])
        row["promotion"] = int(row["promotion"])
    return rows
