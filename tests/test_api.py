"""FastAPI local service contract and guardrail integration tests."""
import unittest
try:
    from fastapi.testclient import TestClient
    from backend.app.main import app
except ImportError:
    TestClient = None

@unittest.skipUnless(TestClient is not None, "Install API dependencies")
class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health(self):
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["mode"], "synthetic-demo")

    def test_catalog(self):
        r = self.client.get("/api/overview")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()["products"]), 8)

    def test_unknown_sku(self):
        self.assertEqual(self.client.get("/api/forecast/NOT-FOUND").status_code, 404)

    def test_pricing_guardrail(self):
        self.assertEqual(self.client.get("/api/pricing/ELEC-101?elasticity=2").status_code, 422)

    def test_stock_nonnegative(self):
        self.assertEqual(self.client.get("/api/inventory/ELEC-101?stock=-1").status_code,422)

    def test_price_changes_are_bounded(self):
        obj=self.client.get("/api/pricing/ELEC-101?elasticity=-1.4").json()
        self.assertTrue(all(abs(x["change_pct"]) <= 10 for x in obj["scenarios"]))

    def test_read_only_methods(self):
        self.assertEqual(self.client.post("/api/pricing/ELEC-101",json={"price":1}).status_code,405)

    def test_frontend_mount(self):
        r=self.client.get("/demo/")
        self.assertEqual(r.status_code,200)
        self.assertIn("INVENTORY",r.text)
        self.assertEqual(self.client.get("/").status_code,200)

if __name__ == "__main__":
    unittest.main()
