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

    def test_reject_unsupported_tag(self):
        with self.assertRaises(ValueError):
            build_report(self.rows,source_label="real-world-validated")

if __name__=="__main__":
    unittest.main()
