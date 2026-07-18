from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.inference.predictor import (
    predict_category
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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