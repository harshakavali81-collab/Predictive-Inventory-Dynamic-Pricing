"""Regression tests using only Python's standard library."""
import unittest
from src.ingestion.generate import generate_sales
from src.processing.validation import validate_sales
from src.forecasting.forecast import predict, backtest, error_metrics
from src.inventory.replenishment import recommend
from src.pricing.scenarios import simulate
from src.pipeline import build_report

class PlanningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sales = generate_sales()

    def test_deterministic_dataset(self):
        self.assertEqual(self.sales, generate_sales())
        self.assertEqual(len(self.sales), 420 * 8)

    def test_validation_and_order(self):
        rows = validate_sales(self.sales)
        self.assertEqual(rows[0]["sku"], "ELEC-101")

    def test_invalid_duplicate(self):
        with self.assertRaises(ValueError):
            validate_sales(self.sales[:1] * 2)

    def test_invalid_negative(self):
        bad = dict(self.sales[0], units=-3)
        with self.assertRaises(ValueError):
            validate_sales([bad])

    def test_naive_repeats_week(self):
        self.assertEqual(predict(list(range(14)), 10, "seasonal_naive"), [float(x) for x in [7,8,9,10,11,12,13,7,8,9]])

    def test_holdout_not_used_for_selection(self):
        values = [10 + (i % 7) * 3 for i in range(140)]
        revised = values[:-28] + [500] * 28
        self.assertEqual(backtest(values)["selected_model"], backtest(revised)["selected_model"])
        self.assertEqual(backtest(values)["validation_mae"], backtest(revised)["validation_mae"])

    def test_no_division_by_zero_wape(self):
        self.assertIsNone(error_metrics([0,0], [1,2])["wape"])

    def test_inventory_reorder(self):
        rec = recommend([20.0] * 28, [20] * 56, 10, 7)
        self.assertGreater(rec["order_quantity"], 0)
        self.assertEqual(rec["safety_stock"], 0)

    def test_inventory_no_order_if_above_point(self):
        rec = recommend([20.0] * 28, [20] * 56, 1000, 7)
        self.assertEqual(rec["order_quantity"], 0)

    def test_stock_invalid(self):
        with self.assertRaises(ValueError):
            recommend([20] * 28, [20] * 56, -2, 7)

    def test_pricing_bounds(self):
        x = simulate(100, 50, 1000)
        self.assertTrue(all(90 <= s["price"] <= 110 for s in x["scenarios"]))
        self.assertTrue(all(s["gross_margin_pct"] >= 20 for s in x["scenarios"]))

    def test_pricing_margin_floor(self):
        x = simulate(100, 85, 500, min_margin=0.10)
        self.assertTrue(all(s["gross_margin_pct"] >= 10 for s in x["scenarios"]))

    def test_pricing_bad_elasticity(self):
        with self.assertRaises(ValueError):
            simulate(100, 50, 100, elasticity=1)

    def test_pipeline_contract(self):
        r = build_report(self.sales)
        self.assertEqual(len(r["products"]), 8)
        self.assertEqual(len(r["products"][0]["model"]["future_forecast"]), 28)
        self.assertIn("synthetic", r["mode"])

if __name__ == "__main__":
    unittest.main()
