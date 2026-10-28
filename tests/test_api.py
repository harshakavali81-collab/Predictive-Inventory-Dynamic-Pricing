"""Optional API integration tests. Run after installing requirements."""
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

if __name__ == "__main__":
    unittest.main()
