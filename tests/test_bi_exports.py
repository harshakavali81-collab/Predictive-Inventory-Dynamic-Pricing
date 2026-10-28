import csv
import tempfile
import unittest
from pathlib import Path
from src.ingestion.generate import generate_sales
from src.pipeline import build_report
from src.analytics.bi_exports import export_powerbi_tables

class PowerBIExportTests(unittest.TestCase):
    def test_model_tables_and_no_double_counting(self):
        sales=generate_sales()
        report=build_report(sales)
        with tempfile.TemporaryDirectory() as folder:
            paths=export_powerbi_tables(sales,report,Path(folder))
            self.assertEqual(len(paths),5)
            asrows=lambda path:list(csv.DictReader(path.open(newline="",encoding="utf-8")))
            tables={p.name:asrows(p) for p in paths}
            self.assertEqual(len(tables["DimProduct.csv"]),8)
            self.assertEqual(len(tables["FactSales.csv"]),3360)
            self.assertEqual(len(tables["FactForecast.csv"]),8*28)
            self.assertEqual(len(tables["FactModelQuality.csv"]),8)
            self.assertTrue(all(x["data_mode"]=="synthetic-demo" for x in tables["FactForecast.csv"]))
            self.assertEqual(sum(int(x["units"]) for x in tables["FactSales.csv"]),report["overview"]["units"])
            self.assertEqual(len({x["date"] for x in tables["DimDate.csv"]}),len(tables["DimDate.csv"]))

if __name__=="__main__":
    unittest.main()
