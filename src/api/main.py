import os
from typing import Optional, List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.inference.predictor import predict_category

app = FastAPI(title="Expense Categorization API", version="v0.4")

# CORS Middleware configuration
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_env == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Request & Response Models
class PredictRequest(BaseModel):
    description: str
    user_id: Optional[str] = None
    custom_rules: Optional[Dict[str, str]] = None


class PredictResponse(BaseModel):
    category: str
    confidence: float
    is_custom_rule: bool


class BatchPredictRequest(BaseModel):
    items: List[PredictRequest]


class BatchPredictResponse(BaseModel):
    predictions: List[PredictResponse]


@app.get("/")
def home():
    return {
        "message": "Expense Categorization API",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {
        "status": "online",
        "model_version": "v0.4"
    }


@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    result = predict_category(
        description=data.description,
        user_id=data.user_id,
        custom_rules=data.custom_rules
    )
    return result


@app.post("/predict-batch", response_model=BatchPredictResponse)
def predict_batch(data: BatchPredictRequest):
    predictions = []
    for item in data.items:
        result = predict_category(
            description=item.description,
            user_id=item.user_id,
            custom_rules=item.custom_rules
        )
        predictions.append(result)
    return {"predictions": predictions}