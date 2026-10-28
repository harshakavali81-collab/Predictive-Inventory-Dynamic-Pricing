-- InventoryIQ analytical warehouse (SQLite 3.35+). Educational local data.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS daily_sales (
  sale_date TEXT NOT NULL CHECK (length(sale_date) = 10),
  sku TEXT NOT NULL CHECK (length(sku) > 0),
  category TEXT NOT NULL,
  units INTEGER NOT NULL CHECK (units >= 0),
  price REAL NOT NULL CHECK (price > 0),
  promotion INTEGER NOT NULL CHECK (promotion IN (0,1)),
  unit_cost REAL NOT NULL CHECK (unit_cost > 0 AND unit_cost < price),
  PRIMARY KEY (sale_date, sku)
);
CREATE INDEX IF NOT EXISTS idx_daily_sales_sku ON daily_sales(sku);
CREATE INDEX IF NOT EXISTS idx_daily_sales_category ON daily_sales(category);
CREATE VIEW IF NOT EXISTS v_daily_kpis AS
 SELECT sale_date, SUM(units) AS units, ROUND(SUM(units*price),2) AS revenue,
 ROUND(SUM(units*(price-unit_cost)),2) AS gross_profit,
 CASE WHEN SUM(units*price)=0 THEN NULL ELSE ROUND(100.0*SUM(units*(price-unit_cost))/SUM(units*price),2) END AS gross_margin_pct
 FROM daily_sales GROUP BY sale_date;
CREATE VIEW IF NOT EXISTS v_sku_kpis AS
 SELECT sku, category, COUNT(*) AS observed_days, SUM(units) AS units,
 ROUND(SUM(units*price),2) AS revenue,
 ROUND(SUM(units*(price-unit_cost)),2) AS gross_profit,
 ROUND(AVG(units),2) AS avg_daily_units
 FROM daily_sales GROUP BY sku,category;
CREATE VIEW IF NOT EXISTS v_promotion_descriptive AS
 SELECT sku, promotion, COUNT(*) AS days, ROUND(AVG(units),2) AS mean_daily_units,
 ROUND(SUM(units*price),2) AS sales_revenue FROM daily_sales GROUP BY sku,promotion;
