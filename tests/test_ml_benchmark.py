"""Optional trained baseline tests; exercised in dedicated ML GitHub Actions workflow."""
import unittest
from datetime import date
from src.forecasting.ml_benchmark import past_features, train_and_evaluate

class MLBenchmarkTests(unittest.TestCase):
    def test_past_features_require_strict_history(self):
        with self.assertRaises(ValueError):
            past_features([20]*28,29,date(2025,1,1))
        self.assertEqual(len(past_features([20]*28,28,date(2025,1,1))),10)

    def test_lag_features_never_read_target(self):
        first=[10 + i%7 for i in range(35)]
        x=past_features(first[:28],28,date(2025,1,1))
        changed=first.copy()
        changed[28]=999
        self.assertEqual(x,past_features(changed[:28],28,date(2025,1,1)))

    def test_training_and_holdout(self):
        try:
            import sklearn
        except ImportError:
            self.skipTest("Optional sklearn dependency not installed")
        values=[14+(i%7)*2 + (i%11)//4 for i in range(140)]
        a=train_and_evaluate(values,n_estimators=16)
        b=train_and_evaluate(values[:-28]+[500]*28,n_estimators=16)
        self.assertEqual(a["predicted"],b["predicted"])
        self.assertEqual(a["training_days"],112)
        self.assertEqual(len(a["actual"]),28)
        self.assertEqual(len(a["predicted"]),28)
        self.assertTrue(all(v>=0 for v in a["predicted"]))

if __name__=="__main__":
    unittest.main()
