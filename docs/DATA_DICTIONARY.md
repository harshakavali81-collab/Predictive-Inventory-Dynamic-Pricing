# Data dictionary

| Field | Type | Meaning |
|---|---|---|
| date | ISO YYYY-MM-DD | Synthetic transaction day |
| sku | string | Unique product identifier |
| category | string | Synthetic merchandise category |
| units | nonnegative integer | Simulated daily sales units |
| price | positive decimal | Synthetic selling price in INR |
| promotion | integer 0/1 | Simulated historical promotion indicator |
| unit_cost | positive decimal | Synthetic per-unit cost in INR |

Grain: unique (date, sku). The `CATALOG` in `src/ingestion/generate.py` additionally defines SKU name, base demand, lead days, inventory and reference price. These catalog fields are manually configured illustrative assumptions. Inventory units are not reconstructed from transaction ledgers.

To use a different CSV, call `src.ingestion.generate.read_csv(path)` and `src.pipeline.build_report(rows)`. The original catalog currently restricts SKUs to the eight configured examples. Real sales would require missing-day handling, returns, refunds, holidays, currency policy and audit trails.

## Imported price treatment

In local CSV import mode, pricing reference price and unit cost come from the **latest date for each SKU** in the imported file. Lead time and on-hand stock remain **illustrative demo catalog values** until replaced with authorized inventory snapshots. Prices in historical imported sales do not establish elasticity or optimal pricing; the simulation uses an explicit assumed elasticity.
