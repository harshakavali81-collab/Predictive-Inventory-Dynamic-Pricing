# Local analytical warehouse

Run `python -m scripts.run_pipeline` to generate:
- `data/generated/synthetic_sales.csv`
- `data/generated/inventoryiq.db` (SQLite, local)
- `data/generated/report.json` (Python holdout and forecast metrics)
- `frontend/report.json` (synthetic safe-to-publish static report)

The SQLite analytical model defined in [sql/schema.sql](../sql/schema.sql) has one daily fact table, a unique `sale_date, sku` key, typed CHECK constraints and daily/SKU/promotion summary views. See [sql/queries.sql](../sql/queries.sql) for KPI reporting examples. This is a documented local warehouse, not a remote warehouse deployment.

Example (install SQLite CLI separately):

```bash
sqlite3 -header -column data/generated/inventoryiq.db "SELECT sku,units,revenue FROM v_sku_kpis ORDER BY revenue DESC;"
sqlite3 data/generated/inventoryiq.db < sql/queries.sql
```

**No causal claims:** Comparing promoted and non-promoted mean units is only descriptive; promotions co-vary with timing, base demand and other confounders.
