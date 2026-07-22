from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_api():
    # 1. Health check
    res_health = client.get("/health")
    print("Health check response:", res_health.json())
    assert res_health.status_code == 200
    assert res_health.json() == {"status": "online", "model_version": "v0.4"}

    # 2. Single Predict
    payload_single = {
        "description": "UPI-STARBUCKS-PAYTM",
        "user_id": "usr_123",
        "custom_rules": {"starbucks": "Client Meetings"}
    }
    res_single = client.post("/predict", json=payload_single)
    print("Single Predict response:", res_single.json())
    assert res_single.status_code == 200
    assert res_single.json()["category"] == "Client Meetings"
    assert res_single.json()["confidence"] == 1.0
    assert res_single.json()["is_custom_rule"] == True

    # 3. Batch Predict
    payload_batch = {
        "items": [
            {
                "description": "UPI-BLINKIT-PAYTM",
                "user_id": "usr_123"
            },
            {
                "description": "UPI-ARPAN KAKKAR-8923824371@IBL",
                "user_id": "usr_123"
            },
            {
                "description": "UPI-STARBUCKS-PAYTM",
                "user_id": "usr_123",
                "custom_rules": {"starbucks": "Client Meetings"}
            }
        ]
    }
    res_batch = client.post("/predict-batch", json=payload_batch)
    print("Batch Predict response:", res_batch.json())
    assert res_batch.status_code == 200
    preds = res_batch.json()["predictions"]
    assert len(preds) == 3
    assert preds[0]["category"] == "Groceries"
    assert preds[0]["is_custom_rule"] == False
    assert preds[1]["category"] == "Transfers"
    assert preds[1]["confidence"] == 1.0
    assert preds[1]["is_custom_rule"] == False
    assert preds[2]["category"] == "Client Meetings"
    assert preds[2]["is_custom_rule"] == True

    print("\nALL API ENDPOINT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_api()
