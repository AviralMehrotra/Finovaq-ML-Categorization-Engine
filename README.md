<p align="center">
  <img src="https://raw.githubusercontent.com/AviralMehrotra/Finovaq/main/public/Finovaq-favicon.png" alt="Finovaq ML Engine" width="72" height="72" />
</p>

<h1 align="center">Finovaq ML Categorization Engine</h1>
<p align="center"><strong>Production-Grade Machine Learning Microservice for Bank Transaction Auto-Categorization</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Scikit--Learn-1.9-F7931E?style=flat-square&logo=scikit-learn" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker" alt="Docker" />
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render" alt="Render" />
  <img src="https://img.shields.io/badge/License-AGPL--3.0-green?style=flat-square" alt="AGPL License" />
</p>

---

## 📌 Overview

The **Finovaq ML Categorization Engine** is a high-performance Python microservice built with **FastAPI**, **Scikit-Learn**, and **TF-IDF Vectorization**. It automatically parses and classifies messy, real-world bank transaction narrations (such as Indian UPI, ACH, IMPS, and credit card strings) into 17 standardized financial categories.

Designed as an external microservice for the [Finovaq Personal Finance SaaS Platform](https://github.com/AviralMehrotra/Finovaq), this backend provides **sub-15ms prediction latency**, **multi-tenant custom user rule overrides**, and **100% confidence P2P transfer resolution**.

---

## ⚡ Key Features

- 🧠 **3-Tier Categorization Pipeline**: Hybrid resolution engine combining user-defined custom rules, regex-based P2P transfer detection, and TF-IDF Logistic Regression ML.
- 🧹 **Robust Banking Preprocessor**: Strips noise like VPAs (`@okicici`, `@ptybl`), 12-digit transaction reference IDs, and repetitive banking prefixes (`UPI`, `NEFT`, `IMPS`, `ACH`).
- ⚡ **High Throughput Batch Endpoint**: Process up to hundreds of transactions in a single HTTP payload (`POST /predict-batch`).
- 🔐 **SaaS Multi-Tenant Isolation**: Supports custom keyword-to-category mapping per user ID.
- 🐳 **Production Docker Containerization**: Lightweight `python:3.12-slim` image bundled with `gunicorn` and `uvicorn` workers.
- 📊 **Sub-15ms Latency**: Ultra-fast execution time per batch prediction.

---

## 🏗️ 3-Tier Categorization Architecture

Every incoming transaction description passes through a deterministic 3-tier evaluation pipeline before invoking the ML model:

```
                      +----------------------------------+
                      |   Incoming Transaction Request   |
                      +----------------------------------+
                                       |
                                       v
                     +------------------------------------+
                     |  Tier 1: Custom User Rule Check    |
                     |  (User-defined keyword match)     |
                     +------------------------------------+
                                 /          \
                       Matched  /            \ Not Matched
                               v              v
               +----------------------+  +------------------------------------+
               | Return Custom Label  |  |   Tier 2: P2P Transfer Engine      |
               | (Confidence: 1.0)    |  |   (Honorific & Personal Name Regex) |
               +----------------------+  +------------------------------------+
                                                     /          \
                                           Matched  /            \ Not Matched
                                                   v              v
                                   +----------------------+  +-----------------------------------+
                                   | Return "Transfers"   |  |   Tier 3: TF-IDF + Scikit-Learn   |
                                   | (Confidence: 1.0)    |  |   Logistic Regression Model (v0.4)|
                                   +----------------------+  +-----------------------------------+
                                                                               |
                                                                               v
                                                                   +-----------------------+
                                                                   | Return Predicted Label|
                                                                   | & Model Confidence    |
                                                                   +-----------------------+
```

---

## 🚀 Model Benchmarks & Metrics

The baseline model was trained on a synthesized dataset of **24,909 realistic bank statement transactions** representing diverse merchant variations, VPAs, and noisy narrations across 17 categories.

| Metric | Score / Benchmark |
|---|---|
| **Model Architecture** | TF-IDF (Sub-word N-Grams 3-5) + Logistic Regression |
| **Dataset Size** | 24,909 rows (balanced synth distribution) |
| **Accuracy** | 98.4% |
| **Macro F1-Score** | 0.98 |
| **Average Latency** | < 15 ms / batch request |
| **Supported Categories** | 17 (Food, Groceries, Travel, Transportation, Shopping, Entertainment, Fuel, Utilities, Bills, Healthcare, Education, Investments, Income, Transfers, Insurance, Housing, Other) |

---

## 📁 Repository Structure

```
expense-categorization-ml/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI server, middleware & Pydantic models
│   ├── inference/
│   │   └── predictor.py         # 3-tier prediction & rule resolution engine
│   └── preprocessing/
│       └── text_cleaner.py      # Banking noise stripper & P2P name detector
│
├── models/
│   ├── v0.4_model.pkl           # Trained Logistic Regression model
│   └── v0.4_vectorizer.pkl      # Fitted TF-IDF Vectorizer
│
├── tests/
│   ├── test_cleaner.py          # Unit tests for preprocessor & regex rules
│   ├── test_predictor.py        # Unit tests for predictor pipeline
│   └── test_api.py              # Integration tests for FastAPI endpoints
│
├── Dockerfile                   # Production Multi-stage Docker image
├── .dockerignore                # Production Docker build exclusions
├── requirements.txt             # Production dependencies (FastAPI, scikit-learn, etc.)
└── requirements-dev.txt         # Dev dependencies (Jupyter, Matplotlib, Pytest)
```

---

## 📡 API Specification

Interactive Swagger UI documentation is available automatically at `/docs` when running the service.

### 1. Health Check
`GET /health`

**Response:**
```json
{
  "status": "online",
  "model_version": "v0.4"
}
```

### 2. Single Prediction
`POST /predict`

**Request Payload:**
```json
{
  "description": "UPI-BLINKIT-PAYTM-BLINKIT@PTYBL-YESB0PTM UPI-122472627770-BLINKIT PAYMENT",
  "user_id": "usr_981273",
  "custom_rules": {
    "starbucks": "Client Meetings"
  }
}
```

**Response:**
```json
{
  "category": "Groceries",
  "confidence": 0.9497,
  "is_custom_rule": false
}
```

### 3. Batch Prediction
`POST /predict-batch`

**Request Payload:**
```json
{
  "items": [
    {
      "description": "UPI-GOOGLE INDIA DIGITAL-GOOG-PAYMENTS@AXISBANK",
      "user_id": "usr_981273"
    },
    {
      "description": "UPI-ARPAN KAKKAR-8923824371@IBL",
      "user_id": "usr_981273"
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "category": "Entertainment",
      "confidence": 0.9977,
      "is_custom_rule": false
    },
    {
      "category": "Transfers",
      "confidence": 1.0,
      "is_custom_rule": false
    }
  ]
}
```

---

## 🛠️ Getting Started

### Local Setup

```bash
# 1. Clone repository
git clone https://github.com/AviralMehrotra/expense-categorization-ml.git
cd expense-categorization-ml

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Start local development server
uvicorn src.api.main:app --reload --port 8000
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

---

### Running Tests

```bash
python -m unittest discover tests
```

---

### 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t finovaq-ml-engine .

# Run container on port 8000
docker run -d -p 8000:8000 --name finovaq-ml finovaq-ml-engine
```

---

## 🌐 Production Deployment (Render)

This repository is configured out-of-the-box for [Render](https://render.com).

1. Create a **New Web Service** on Render and connect your GitHub repo.
2. Set **Build Command**: `pip install -r requirements.txt`
3. Set **Start Command**: `gunicorn src.api.main:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`
4. Deploy!

---

## 📄 License

This project is open-source and available under the [AGPL-3.0 License](LICENSE).
