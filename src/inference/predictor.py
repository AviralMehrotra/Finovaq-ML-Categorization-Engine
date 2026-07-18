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


def predict_category(description):
    # Rule-based shortcut: detect personal P2P transfers before hitting the model
    if is_personal_transfer(description):
        return {
            "category": "Transfers",
            "confidence": 1.0
        }

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
        )
    }