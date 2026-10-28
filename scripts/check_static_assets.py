"""Dependency-free validation of the static sample and original SVG illustrations."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]

class StaticAssetTests(unittest.TestCase):
    def test_original_diagrams_xml(self):
        files=sorted((ROOT/"docs/visuals").glob("*.svg"))
        self.assertEqual(len(files),10)
        for f in files:
            root=ET.parse(f).getroot()
            self.assertTrue(root.tag.endswith("svg"),f.name)
            self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"),f.name)

    def test_dashboard_accessibility_contract(self):
        html=(ROOT/"frontend/index.html").read_text(encoding="utf-8")
        js=(ROOT/"frontend/app.js").read_text(encoding="utf-8")
        self.assertIn('id="trend-chart"',html)
        self.assertIn('id="advanced-planner"',html)
        self.assertIn('id="model-proof"',html)
        self.assertIn('id="download-forecast"',html)
        self.assertIn('role="status"',html)
        self.assertIn('id="data-status"',html)
        self.assertIn('id="interval-note"',html)
        self.assertIn('data.mode!=="synthetic-demo"',js)
        self.assertIn('model.holdout_interval_coverage',js)

    def test_hosting_entrypoints(self):
        self.assertTrue((ROOT/"demo.html").is_file())
        self.assertIn("frontend/",(ROOT/"demo.html").read_text())
        self.assertTrue((ROOT/".github/workflows/pages.yml").is_file())

if __name__=="__main__":
    unittest.main()
