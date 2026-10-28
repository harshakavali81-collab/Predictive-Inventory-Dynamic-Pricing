# InventoryIQ — API contract

The FastAPI app is **read-only**, backed by deterministic sample catalog values and synthetic generated transactions. The OpenAPI contract is available locally at `http://127.0.0.1:8000/docs`.

| GET endpoint | Function | Notes |
|---|---|---|
| `/api/health` | Static health and data-mode marker | Not a full production dependency check |
| `/api/overview` | 8-SKU overview | Synthetic performance, indicative stock exposure |
| `/api/forecast/ELEC-101` | Full historical, 28-day point and error-band forecasts | Bands descriptive; no guaranteed 90% coverage |
| `/api/inventory/ELEC-101?stock=210` | Simple reorder heuristic | Stock override is illustrative |
| `/api/inventory/ELEC-101/plan?stock=210&on_order=0&allocated=0&backorders=0&pack_size=6&max_order=1000` | Advanced order what-if | Uses inventory position, rounds to pack size, caps orders, marks shortages |
| `/api/pricing/ELEC-101?elasticity=-1.4` | Marginal scenario table | Assumed elasticity only |

HTTP 422 is returned for invalid numeric parameters or impossible allocations; 404 for nonexistent SKU. HTTP POST/PATCH/DELETE are not implemented; no prices, orders or customer information are persisted by the API.

The backend is not hardened for public exposure; it is intended for local educational demonstration. Keep binding to loopback, apply authenticated controls and operational integration testing before using any external deployment.
