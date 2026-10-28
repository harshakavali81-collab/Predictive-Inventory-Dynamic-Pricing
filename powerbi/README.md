# InventoryIQ — reproducible Power BI data model

This repository generates **Power BI-ready star-schema CSV files**, not a native `.pbix` file. All included example data is synthetic. Run:

```bash
python -m scripts.run_pipeline
```

Look under `data/generated/bi/`:

| Table | Grain | Usage |
|---|---|---|
| DimDate | one calendar date | Calendar dimension for sales and forecasts |
| DimProduct | one SKU | Product category, example cost, lead time |
| FactSales | one SKU + day | Sales units, promo, revenue, gross profit |
| FactForecast | one SKU + future day | Python pipeline's 28-day demand forecast |
| FactModelQuality | one SKU | Selected model and holdout MAE/WAPE/sMAPE |
| FactInventory | one SKU | Illustrative on-hand, lead time, reorder level and suggested quantity |
| FactPricingScenario | one SKU + allowed price change | Hypothetical price, units, gross profit and modeled margin |

## Desktop instructions

1. In Power BI Desktop, choose Get data → Text/CSV to load all seven CSVs.
2. Set `date` columns to **Date** and `sku` columns to **Text**. Numeric revenue/profit/units fields should be Decimal/Whole Number.
3. Set `DimDate[date]` as the marked Date table. Create one-to-many relationships `DimDate[date] → FactSales[date]` and `DimDate[date] → FactForecast[date]`. Set `DimProduct[sku]` to one-to-many with the two fact tables plus `FactModelQuality`, `FactInventory`, and `FactPricingScenario`. Use **single-direction** filtering to avoid ambiguous paths.
4. Create KPI cards for revenue, profit, demand forecast, WAPE and stock cover. Add time-series charts for sales and forecast with an explicit forecast period.
5. Label each page **Synthetic / demonstration only** and note WAPE is an evaluation metric for simulated holdout data, not a confidence bound.

## Useful DAX

```dax
Revenue = SUM(FactSales[revenue])
Gross Profit = SUM(FactSales[gross_profit])
Units Sold = SUM(FactSales[units])
Gross Margin % = DIVIDE([Gross Profit], [Revenue])
Forecast Units = SUM(FactForecast[forecast_units])
Forecast WAPE % = AVERAGE(FactModelQuality[holdout_wape_pct])
Suggested Order Units = SUM(FactInventory[suggested_order])
Scenario Gross Profit = SUM(FactPricingScenario[projected_profit])
```

The last WAPE example is the **unweighted SKU average**, suitable only when explicitly labelled. For a unit-weighted aggregate, compute total absolute errors / total actual units from exported sealed-holdout details instead of averaging percentages.

## Proposed pages

- **Executive overview:** units, revenue, gross profit, historical demand.
- **Forecast diagnostics:** daily sales vs projected demand, methods and sealed test WAPE.
- **Inventory policy:** stock, reorder point and lead time (derived from report.json; not full transaction ledgers).
- **Pricing what-ifs:** candidate prices with assumed elasticity and margin guardrails.

A Power BI Desktop-created `.pbix` is not bundled and is not claimed tested; producing one requires the Desktop application or a supported report-authoring service.

## Analytical caveat for scenario tables

`FactPricingScenario` contains multiple mutually exclusive what-if candidates for each SKU, so summing all candidate profits across the table **double counts** incompatible scenarios. Filter to exactly one scenario per SKU, or the `recommended_under_assumption = 1` indicator, before reporting any scenario portfolio total. Even then the outcome remains hypothetical. Inventory values use an example catalog, not a reconciled stock ledger.
