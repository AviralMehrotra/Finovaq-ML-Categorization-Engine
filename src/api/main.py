from fastapi import FastAPI

from src.inference.predictor import (
    predict_category
)

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Expense Categorization API"
    }

@app.post("/predict")
def predict(data: dict):
    description = data["description"]
    result = predict_category(
        description
    )
    return result