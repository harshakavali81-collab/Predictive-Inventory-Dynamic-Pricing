"""Extended review-only inventory-position planning.

Inventory position = on hand - allocations + on order - backorders.
All values must be operator-verified before use; no fulfillment operations occur.
"""
from __future__ import annotations
from math import ceil
from src.inventory.replenishment import recommend

def plan_order(forecast: list[float], historical_units: list[int], *, on_hand: int,
               lead_days: int, on_order: int = 0, allocated: int = 0,
               backorders: int = 0, pack_size: int = 1, max_order: int = 10000,
               review_days: int = 7, service_level: float = 0.95) -> dict:
    for name,value in {
        "on_order":on_order, "allocated":allocated, "backorders":backorders,
        "pack_size":pack_size, "max_order":max_order
    }.items():
        if type(value) is not int or not 0 <= value <= 10_000_000:
            raise ValueError(f"{name} must be a nonnegative integer <= 10,000,000")
    if pack_size < 1:
        raise ValueError("pack_size must be positive")
    if allocated > on_hand:
        raise ValueError("Allocated inventory cannot exceed on-hand in this simplified model")
    base = recommend(forecast, historical_units, on_hand, lead_days, review_days, service_level)
    position = on_hand - allocated + on_order - backorders
    trigger = position <= base["reorder_point"]
    needed = max(0, base["target_stock"] - position) if trigger else 0
    packs = ceil(needed / pack_size) if needed else 0
    suggested = min(packs * pack_size, (max_order // pack_size) * pack_size)
    limited = suggested < needed
    return {
        **base,
        "on_order": on_order, "allocated": allocated, "backorders": backorders,
        "inventory_position": position, "reorder_triggered": trigger,
        "unrounded_need": needed, "order_quantity": suggested, "pack_size": pack_size,
        "max_order": max_order, "quantity_limited": limited,
        "manual_review_required": bool(limited or position < 0),
        "policy": "Inventory-position, pack-rounded, capped and review-only",
        "note": "What-if policy, not an executable purchase order. Verify stock accuracy, lead times, backlog, pack sizes, budgets, and real service levels."
    }
