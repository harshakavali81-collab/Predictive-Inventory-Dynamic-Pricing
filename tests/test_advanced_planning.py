import unittest
from src.inventory.position import plan_order
from src.forecasting.forecast import backtest
from src.forecasting.uncertainty import residual_band, observed_coverage

class AdvancedTests(unittest.TestCase):
    def setUp(self):
        self.future=[20.0]*28
        self.history=[20]*56

    def test_on_order_reduces_required_quantity(self):
        a=plan_order(self.future,self.history,on_hand=10,lead_days=7)
        b=plan_order(self.future,self.history,on_hand=10,lead_days=7,on_order=80)
        self.assertLess(b["order_quantity"],a["order_quantity"])
        self.assertEqual(b["inventory_position"],90)

    def test_allocation_backlog_affects_position(self):
        a=plan_order(self.future,self.history,on_hand=100,lead_days=7,
                     allocated=30,backorders=5,on_order=25)
        self.assertEqual(a["inventory_position"],90)

    def test_pack_multiple(self):
        a=plan_order(self.future,self.history,on_hand=1,lead_days=7,pack_size=12)
        self.assertEqual(a["order_quantity"]%12,0)

    def test_cap_triggers_review(self):
        a=plan_order(self.future,self.history,on_hand=1,lead_days=7,pack_size=12,max_order=48)
        self.assertEqual(a["order_quantity"],48)
        self.assertTrue(a["manual_review_required"])

    def test_reject_overallocated(self):
        with self.assertRaises(ValueError):
            plan_order(self.future,self.history,on_hand=3,lead_days=7,allocated=5)

    def test_no_order_above_point(self):
        a=plan_order(self.future,self.history,on_hand=999,lead_days=7)
        self.assertFalse(a["reorder_triggered"])
        self.assertEqual(a["order_quantity"],0)

    def test_descriptive_band_nonnegative(self):
        b=residual_band([1,3,4,10,2,1,4,2,4,3],[0,5,20],0.9)
        self.assertEqual(len(b["lower"]),3)
        self.assertEqual(b["lower"][0],0)
        self.assertTrue(all(y>=x for x,y in zip(b["lower"],b["upper"])))

    def test_invalid_residual(self):
        with self.assertRaises(ValueError):
            residual_band([float("nan")],[2.0])

    def test_holdout_coverage(self):
        values=[15+(i%7)*2 for i in range(140)]
        a=backtest(values)
        b=backtest(values[:-28]+[500]*28)
        self.assertEqual(a["future_interval"]["absolute_error_width"],b["future_interval"]["absolute_error_width"])
        self.assertTrue(0<=a["holdout_interval_coverage"]<=1)

    def test_observed_coverage_exact(self):
        self.assertEqual(observed_coverage([0,10,20],[0,10,21],[1,10,30]),0.667)

if __name__=="__main__":
    unittest.main()
