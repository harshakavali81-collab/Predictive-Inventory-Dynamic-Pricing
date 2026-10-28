# Power BI preparation — import guide (no .pbix included)

The pipeline creates `data/generated/synthetic_sales.csv`. Import through **Power BI Desktop → Get data → Text/CSV**. Verify types: date=Date, units=Whole number, price and unit_cost=Decimal number, promotion=Whole number. Create a calendar/date table and a one-to-many relationship to the sales date.

Suggested measures (rename the table if needed):

```dax
Revenue = SUMX(Sales, Sales[units] * Sales[price])
Gross Profit = SUMX(Sales, Sales[units] * (Sales[price] - Sales[unit_cost]))
Units Sold = SUM(Sales[units])
Gross Margin % = DIVIDE([Gross Profit], [Revenue])
Average Price = DIVIDE([Revenue], [Units Sold])
```

Build pages for revenue by category, daily demand and promotional mix. Use slicers for SKU, category, month and promotion. *A native PBIX file has not been built or validated in Power BI Desktop.*
