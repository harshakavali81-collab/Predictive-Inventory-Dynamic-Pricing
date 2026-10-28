-- Run through sqlite3 data/generated/inventoryiq.db < sql/queries.sql
-- 1. All-SKU KPIs
SELECT * FROM v_sku_kpis ORDER BY revenue DESC;

-- 2. Last 14 days of aggregate trading
SELECT * FROM v_daily_kpis ORDER BY sale_date DESC LIMIT 14;

-- 3. Descriptive promotions (DOES NOT identify causal uplift)
SELECT * FROM v_promotion_descriptive ORDER BY sku,promotion;

-- 4. Stock category concentration
SELECT category, SUM(units) AS units, ROUND(SUM(units * price),2) AS revenue,
 ROUND(100.0 * SUM(units * price) / NULLIF((SELECT SUM(units * price) FROM daily_sales),0),2) AS revenue_share_pct
 FROM daily_sales GROUP BY category ORDER BY revenue DESC;

-- 5. Weekly units by SKU
SELECT sku, strftime('%Y-%W', sale_date) AS year_week,
 SUM(units) AS units, ROUND(SUM(units * price),2) AS revenue
 FROM daily_sales GROUP BY sku, year_week ORDER BY sku, year_week;
