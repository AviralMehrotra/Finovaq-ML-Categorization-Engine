import joblib
import os

from src.preprocessing.text_cleaner import clean_text


MODELS_DIR = "models"
LR_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "v0.3_model.pkl"
)
VECTORIZER_PATH = os.path.join(
    MODELS_DIR,
    "v0.3_vectorizer.pkl"
)


model = joblib.load(LR_MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_category(description):
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