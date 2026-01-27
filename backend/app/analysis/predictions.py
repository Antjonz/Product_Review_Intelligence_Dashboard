import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge

from .sentiment import get_sentiment


class RatingPredictor:
    def __init__(self):
        self._vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")
        self._model = Ridge(alpha=1.0)
        self._fitted = False

    def fit(self, texts: list[str], ratings: list[int]):
        if len(texts) < 10:
            return
        X = self._vectorizer.fit_transform(texts)
        self._model.fit(X, ratings)
        self._fitted = True

    def predict(self, text: str) -> dict:
        sentiment = get_sentiment(text)
        if not self._fitted:
            # Fallback: estimate from sentiment
            predicted = 3.0 + sentiment["score"] * 2.0
            return {
                "predicted_rating": round(max(1.0, min(5.0, predicted)), 1),
                "confidence": 0.4,
                "sentiment": sentiment["label"],
                "sentiment_score": round(sentiment["score"], 3),
            }

        X = self._vectorizer.transform([text])
        pred = self._model.predict(X)[0]
        pred = max(1.0, min(5.0, pred))

        # Simple confidence based on how close to integer
        nearest_int = round(pred)
        confidence = max(0.5, 1.0 - abs(pred - nearest_int) * 0.5)

        return {
            "predicted_rating": round(pred, 1),
            "confidence": round(confidence, 2),
            "sentiment": sentiment["label"],
            "sentiment_score": round(sentiment["score"], 3),
        }


# Singleton predictor
predictor = RatingPredictor()
