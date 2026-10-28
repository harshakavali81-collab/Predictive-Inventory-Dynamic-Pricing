"""Read-only API and local demonstration static UI. Synthetic data only."""
from functools import lru_cache
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.pipeline import build_report
from src.inventory.replenishment import recommend
from src.inventory.position import plan_order
from src.pricing.scenarios import simulate

app = FastAPI(title="InventoryIQ | Demand, Stock and Pricing API", version="1.1.0",
              description="Synthetic-data educational prototype. No automated price or stock changes.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8000", "http://127.0.0.1:8000",
    "http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["GET"], allow_headers=["*"])

@lru_cache(maxsize=1)
def report():
    return build_report()

def product(sku: str):
    for item in report()["products"]:
        if item["sku"] == sku:
            return item
    raise HTTPException(404, "Unknown SKU")

@app.get("/")
def home():
    return RedirectResponse(url="/demo/", status_code=307)

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "synthetic-demo"}

@app.get("/api/overview")
def overview():
    r = report()
    return {"as_of": r["as_of"], "overview": r["overview"],
            "products": [{"sku": p["sku"], "name": p["name"],
                "wape": p["model"]["holdout"]["wape"],
                "order_quantity": p["inventory"]["order_quantity"],
                "risk": p["inventory"]["stockout_risk_proxy"]} for p in r["products"]],
            "limitations": r["limitations"]}

@app.get("/api/forecast/{sku}")
def forecast(sku: str):
    p = product(sku)
    return {"sku": sku, "dates": p["forecast_dates"], "model": p["model"], "history": p["history"]}

@app.get("/api/inventory/{sku}")
def inventory(sku: str, stock: int | None = Query(default=None, ge=0, le=10000000)):
    p = product(sku)
    if stock is None:
        return p["inventory"]
    from src.ingestion.generate import CATALOG
    lead_days = next(x["lead_days"] for x in CATALOG if x["sku"] == sku)
    return recommend(p["model"]["future_forecast"], [r["units"] for r in p["history"]],
                     stock, lead_days)

@app.get("/api/pricing/{sku}")
def pricing(sku: str, elasticity: float = Query(default=-1.4, ge=-4, le=-0.1)):
    p = product(sku)
    return simulate(p["price"], p["cost"], sum(p["model"]["future_forecast"]), elasticity)


@app.get("/api/inventory/{sku}/plan")
def inventory_plan(sku: str,
                   stock: int = Query(ge=0, le=1000000),
                   on_order: int = Query(default=0, ge=0, le=1000000),
                   allocated: int = Query(default=0, ge=0, le=1000000),
                   backorders: int = Query(default=0, ge=0, le=1000000),
                   pack_size: int = Query(default=1, ge=1, le=10000),
                   max_order: int = Query(default=10000, ge=0, le=1000000)):
    """Read-only inventory-position scenarios, never actual purchase orders."""
    p = product(sku)
    from src.ingestion.generate import CATALOG
    lead = next(c["lead_days"] for c in CATALOG if c["sku"] == sku)
    if allocated > stock:
        raise HTTPException(status_code=422, detail="Allocated stock exceeds on-hand quantity")
    return plan_order(p["model"]["future_forecast"], [r["units"] for r in p["history"]],
                      on_hand=stock, lead_days=lead, on_order=on_order, allocated=allocated,
                      backorders=backorders, pack_size=pack_size, max_order=max_order)

# The generated synthetic report is a static asset for the same-origin frontend.
# Nothing accepts edits or executes operational price/stock changes.
app.mount("/demo", StaticFiles(directory=str(Path(__file__).resolve().parents[2] / "frontend"),
                               html=True), name="demo")
