import unittest
from fastapi.testclient import TestClient
from src.api.main import app


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_home_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("version", data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertEqual(data["model_version"], "v0.4")

    def test_predict_single_endpoint(self):
        payload = {
            "description": "UPI-STARBUCKS-PAYTM",
            "user_id": "usr_123",
            "custom_rules": {"starbucks": "Client Meetings"}
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["category"], "Client Meetings")
        self.assertEqual(data["confidence"], 1.0)
        self.assertTrue(data["is_custom_rule"])

    def test_predict_batch_endpoint(self):
        payload = {
            "items": [
                {
                    "description": "UPI-BLINKIT-PAYTM",
                    "user_id": "usr_123"
                },
                {
                    "description": "UPI-ARPAN KAKKAR-8923824371@IBL",
                    "user_id": "usr_123"
                }
            ]
        }
        response = self.client.post("/predict-batch", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["predictions"]), 2)
        self.assertEqual(data["predictions"][0]["category"], "Groceries")
        self.assertEqual(data["predictions"][1]["category"], "Transfers")


if __name__ == "__main__":
    unittest.main()
