import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def get_sentiment(text: str) -> dict:
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {"score": compound, "label": label}


def analyze_sentiments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    results = df["review_text"].apply(get_sentiment)
    df["sentiment_score"] = results.apply(lambda x: x["score"])
    df["sentiment"] = results.apply(lambda x: x["label"])
    return df


def build_sentiment_timeline(df: pd.DataFrame) -> list[dict]:
    if "date" not in df.columns or df["date"].isna().all():
        # Create synthetic timeline by splitting into 12 chunks
        n = len(df)
        chunk_size = max(1, n // 12)
        timeline = []
        for i in range(0, n, chunk_size):
            chunk = df.iloc[i : i + chunk_size]
            period_label = f"Batch {i // chunk_size + 1}"
            total = len(chunk)
            if total == 0:
                continue
            timeline.append(
                {
                    "period": period_label,
                    "positive": round((chunk["sentiment"] == "positive").sum() / total * 100, 1),
                    "negative": round((chunk["sentiment"] == "negative").sum() / total * 100, 1),
                    "neutral": round((chunk["sentiment"] == "neutral").sum() / total * 100, 1),
                    "avg_sentiment": round(chunk["sentiment_score"].mean(), 3),
                }
            )
        return timeline

    df_dated = df.dropna(subset=["date"]).copy()
    df_dated = df_dated.sort_values("date")
    df_dated["period"] = df_dated["date"].dt.to_period("M").astype(str)

    timeline = []
    for period, group in df_dated.groupby("period"):
        total = len(group)
        timeline.append(
            {
                "period": period,
                "positive": round((group["sentiment"] == "positive").sum() / total * 100, 1),
                "negative": round((group["sentiment"] == "negative").sum() / total * 100, 1),
                "neutral": round((group["sentiment"] == "neutral").sum() / total * 100, 1),
                "avg_sentiment": round(group["sentiment_score"].mean(), 3),
            }
        )
    return timeline


def get_sentiment_breakdown(df: pd.DataFrame) -> dict[str, int]:
    counts = df["sentiment"].value_counts().to_dict()
    return {
        "positive": int(counts.get("positive", 0)),
        "negative": int(counts.get("negative", 0)),
        "neutral": int(counts.get("neutral", 0)),
    }
