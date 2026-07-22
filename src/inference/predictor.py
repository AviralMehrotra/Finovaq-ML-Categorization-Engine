import joblib
import os

from src.preprocessing.text_cleaner import clean_text, is_personal_transfer


MODELS_DIR = "models"
LR_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "v0.4_model.pkl"
)
VECTORIZER_PATH = os.path.join(
    MODELS_DIR,
    "v0.4_vectorizer.pkl"
)


model = joblib.load(LR_MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_category(description: str, user_id: str = None, custom_rules: dict = None):
    # Rule Step 1: Custom User Rule Overrides Check
    if custom_rules:
        cleaned_text = clean_text(description)
        desc_lower = description.lower()
        for keyword, rule_category in custom_rules.items():
            kw_lower = keyword.lower().strip()
            if kw_lower and (kw_lower in cleaned_text or kw_lower in desc_lower):
                return {
                    "category": rule_category,
                    "confidence": 1.0,
                    "is_custom_rule": True
                }

    # Rule Step 2: P2P Transfer Check
    if is_personal_transfer(description):
        return {
            "category": "Transfers",
            "confidence": 1.0,
            "is_custom_rule": False
        }

    # ML Step 3: Model Inference
    cleaned_text = clean_text(description)

    vector = vectorizer.transform(
        [cleaned_text]
    )

    prediction = model.predict(
        vector
    )[0]

    confidence = max(
        model.predict_proba(vector)[0]
    )

    return {
        "category": prediction,
        "confidence": round(
            float(confidence),
            4
        ),
        "is_custom_rule": False
    }