import os
import time
import logging
from typing import Optional, List, Dict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.inference.predictor import predict_category

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("categorization-service")

tags_metadata = [
    {
        "name": "Health",
        "description": "System health and status monitoring.",
    },
    {
        "name": "Prediction",
        "description": "Single and batch ML transaction categorization endpoints.",
    },
]

app = FastAPI(
    title="Finovaq ML Categorization Engine",
    description="High-performance machine learning microservice for bank transaction auto-categorization.",
    version="v0.4",
    openapi_tags=tags_metadata,
)

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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # in ms
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    logger.info(f"Path: {request.url.path} | Method: {request.method} | Status: {response.status_code} | Latency: {process_time:.2f}ms")
    return response


# Pydantic Request & Response Models with Examples
class PredictRequest(BaseModel):
    description: str = Field(
        ...,
        description="Raw bank transaction narration string",
        example="UPI-BLINKIT-PAYTM-BLINKIT@PTYBL-YESB0PTM UPI-122472627770-BLINKIT PAYMENT"
    )
    user_id: Optional[str] = Field(
        None,
        description="Optional user ID for multi-tenant isolation",
        example="usr_981273"
    )
    custom_rules: Optional[Dict[str, str]] = Field(
        None,
        description="User custom keyword to category mappings",
        example={"starbucks": "Meetings", "blinkit": "Quick Commerce"}
    )


class PredictResponse(BaseModel):
    category: str = Field(..., description="Categorized expense label", example="Groceries")
    confidence: float = Field(..., description="Prediction confidence score between 0.0 and 1.0", example=0.9497)
    is_custom_rule: bool = Field(..., description="Whether category was resolved via custom user rule", example=False)


class BatchPredictRequest(BaseModel):
    items: List[PredictRequest] = Field(..., description="List of transaction requests")


class BatchPredictResponse(BaseModel):
    predictions: List[PredictResponse]


@app.get("/", tags=["Health"])
def home():
    return {
        "service": "Finovaq ML Categorization Engine",
        "status": "online",
        "version": "v0.4"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "model_version": "v0.4"
    }


@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
def predict(data: PredictRequest):
    result = predict_category(
        description=data.description,
        user_id=data.user_id,
        custom_rules=data.custom_rules
    )
    return result


@app.post("/predict-batch", response_model=BatchPredictResponse, tags=["Prediction"])
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