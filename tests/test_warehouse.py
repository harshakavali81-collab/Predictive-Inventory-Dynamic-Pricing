"""Data quality, SQLite and controlled CSV input regression tests."""
import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path
from src.ingestion.generate import generate_sales, save_csv, read_csv
from src.analytics.report import summarize
from src.analytics.warehouse import export_warehouse, query_kpis
from src.pipeline import build_report
from scripts.run_pipeline import validate_continuous_daily_history, main

class WarehouseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sales = generate_sales()

    def test_sqlite_consistent_with_python(self):
        with tempfile.TemporaryDirectory() as d:
            target = export_warehouse(self.sales, Path(d)/"warehouse.sqlite")
            rows = query_kpis(target)
            kpis = summarize(self.sales)
            self.assertEqual(sum(x["units"] for x in rows), kpis["units"])
            with sqlite3.connect(target) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM daily_sales").fetchone()[0],len(self.sales))
                sql_revenue=db.execute("SELECT ROUND(SUM(revenue),2) FROM v_sku_kpis").fetchone()[0]
            self.assertAlmostEqual(sql_revenue,kpis["revenue"],places=2)

    def test_csv_import(self):
        with tempfile.TemporaryDirectory() as d:
            path=save_csv(self.sales,Path(d)/"sales.csv")
            imported=read_csv(path)
            self.assertEqual(imported,self.sales)
            self.assertEqual(build_report(imported,source_label="imported-local-csv")["mode"],"imported-local-csv")

    def test_history_missing_date_is_rejected(self):
        shortened=[x for x in self.sales if not (x["sku"]=="ELEC-101" and x["date"]=="2025-02-01")]
        with self.assertRaisesRegex(ValueError,"missing daily dates"):
            validate_continuous_daily_history(shortened)

    def test_short_history_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"120"):
            validate_continuous_daily_history(self.sales[:20])

    def test_imported_csv_never_published_to_frontend(self):
        with tempfile.TemporaryDirectory() as d:
            path=save_csv(self.sales,Path(d)/"sales.csv")
            with self.assertRaisesRegex(ValueError,"public frontend"):
                main(["--input",str(path),"--output","frontend/imported-report.json"])

    def test_local_import_with_local_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            path=save_csv(self.sales,Path(d)/"sales.csv")
            output=Path(d)/"local.json"
            db=Path(d)/"local.sqlite"
            main(["--input",str(path),"--output",str(output),"--sqlite",str(db)])
            self.assertTrue(output.is_file())
            self.assertTrue(db.is_file())
            self.assertIn("imported-local-csv",output.read_text())

if __name__=="__main__":
    unittest.main()
