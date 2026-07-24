import unittest
from src.inference.predictor import predict_category


class TestPredictor(unittest.TestCase):

    def test_custom_rule_override(self):
        custom_rules = {"starbucks": "Client Meetings"}
        res = predict_category("UPI-STARBUCKS-PAYTM", custom_rules=custom_rules)
        self.assertEqual(res["category"], "Client Meetings")
        self.assertEqual(res["confidence"], 1.0)
        self.assertTrue(res["is_custom_rule"])

    def test_personal_transfer_shortcut(self):
        res = predict_category("UPI-ARPAN KAKKAR-8923824371@IBL-ICIC0001047")
        self.assertEqual(res["category"], "Transfers")
        self.assertEqual(res["confidence"], 1.0)
        self.assertFalse(res["is_custom_rule"])

    def test_ml_model_prediction(self):
        res = predict_category("UPI-BLINKIT-PAYTM-BLINKIT@PTYBL-YESB0PTM UPI-122472627770-BLINKIT PAYMENT")
        self.assertEqual(res["category"], "Groceries")
        self.assertGreater(res["confidence"], 0.8)
        self.assertFalse(res["is_custom_rule"])


if __name__ == "__main__":
    unittest.main()
