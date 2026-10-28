"""Prevent imported local data from being mislabelled synthetic or made public."""
import unittest
from src.ingestion.generate import generate_sales
from src.pipeline import build_report
from src.analytics.report import summarize

class ProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=generate_sales()

    def test_synthetic_tag(self):
        r=build_report(self.rows)
        self.assertEqual(r["overview"]["data_source"],"synthetic-demo")

    def test_imported_tag(self):
        r=build_report(self.rows,source_label="imported-local-csv")
        self.assertEqual(r["overview"]["data_source"],"imported-local-csv")
        self.assertIn("unverified",r["generated_from"])
        self.assertEqual(r["products"][0]["reference_price_source"],"most_recent_observation")

    def test_imported_price_uses_latest_record(self):
        custom=[dict(row) for row in self.rows]
        target=max((r for r in custom if r["sku"]=="ELEC-101"),key=lambda r:r["date"])
        target["price"]=3999.0
        target["unit_cost"]=1700.0
        imported=build_report(custom,source_label="imported-local-csv")
        synthetic=build_report(self.rows)
        p=next(x for x in imported["products"] if x["sku"]=="ELEC-101")
        baseline=next(x for x in synthetic["products"] if x["sku"]=="ELEC-101")
        self.assertEqual(p["price"],3999.0)
        self.assertEqual(p["cost"],1700.0)
        self.assertNotEqual(p["price"],baseline["price"])

    def test_reject_unsupported_tag(self):
        with self.assertRaises(ValueError):
            build_report(self.rows,source_label="real-world-validated")

if __name__=="__main__":
    unittest.main()
