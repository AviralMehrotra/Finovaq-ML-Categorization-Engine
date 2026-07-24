import unittest
from src.preprocessing.text_cleaner import clean_text, is_personal_transfer


class TestTextCleaner(unittest.TestCase):

    def test_clean_text_strips_vpa_and_transaction_ids(self):
        raw = "UPI-BLINKIT-PAYTM-BLINKIT@PTYBL-YESB0PTM UPI-122472627770-BLINKIT PAYMENT"
        cleaned = clean_text(raw)
        self.assertNotIn("122472627770", cleaned)
        self.assertNotIn("ptybl", cleaned)
        self.assertIn("blinkit", cleaned)

    def test_is_personal_transfer_detects_individual_names(self):
        self.assertTrue(is_personal_transfer("UPI-ARPAN KAKKAR-8923824371@IBL-ICIC0001047"))
        self.assertTrue(is_personal_transfer("UPI-MRS ANAMIKA MEHROTRA-ANAMIKAMEHROTRA521@OKSBI"))
        self.assertTrue(is_personal_transfer("UPI-MR AMIT SINGH-000U528@OKICICI"))

    def test_is_personal_transfer_ignores_businesses(self):
        self.assertFalse(is_personal_transfer("UPI-GOOGLE INDIA DIGITAL-GOOG@AXISBANK"))
        self.assertFalse(is_personal_transfer("UPI-DELHIVERY LIMITED-PAYTM"))
        self.assertFalse(is_personal_transfer("UPI-AMAZON PAY GROCERIES-AMAZONPAYGROCERY@APL"))
        self.assertFalse(is_personal_transfer("UPI-NATRAJ BOOK POINT-PAYTM"))


if __name__ == "__main__":
    unittest.main()
