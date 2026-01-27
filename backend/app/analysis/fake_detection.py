import numpy as np
import pandas as pd


def detect_fake_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fake_score"] = 0.0
    df["fake_reasons"] = [[] for _ in range(len(df))]

    # 1) Very short reviews (< 20 chars)
    short_mask = df["review_text"].str.len() < 20
    df.loc[short_mask, "fake_score"] += 0.3
    for idx in df.index[short_mask]:
        df.at[idx, "fake_reasons"].append("Very short review")

    # 2) Sentiment-rating mismatch
    if "sentiment_score" in df.columns:
        # Positive sentiment but low rating
        mismatch1 = (df["sentiment_score"] > 0.5) & (df["rating"] <= 2)
        df.loc[mismatch1, "fake_score"] += 0.35
        for idx in df.index[mismatch1]:
            df.at[idx, "fake_reasons"].append("Positive text but low rating")

        # Negative sentiment but high rating
        mismatch2 = (df["sentiment_score"] < -0.5) & (df["rating"] >= 4)
        df.loc[mismatch2, "fake_score"] += 0.35
        for idx in df.index[mismatch2]:
            df.at[idx, "fake_reasons"].append("Negative text but high rating")

    # 3) Extreme sentiment (very robotic / over-the-top)
    if "sentiment_score" in df.columns:
        extreme = df["sentiment_score"].abs() > 0.95
        df.loc[extreme, "fake_score"] += 0.15
        for idx in df.index[extreme]:
            df.at[idx, "fake_reasons"].append("Extremely polarized sentiment")

    # 4) All caps text
    caps_ratio = df["review_text"].apply(
        lambda x: sum(1 for c in x if c.isupper()) / max(len(x), 1)
    )
    caps_mask = caps_ratio > 0.6
    df.loc[caps_mask, "fake_score"] += 0.2
    for idx in df.index[caps_mask]:
        df.at[idx, "fake_reasons"].append("Excessive capitalization")

    # 5) Repetitive characters / words
    def has_repetition(text: str) -> bool:
        words = text.lower().split()
        if len(words) < 3:
            return False
        unique_ratio = len(set(words)) / len(words)
        return unique_ratio < 0.4

    rep_mask = df["review_text"].apply(has_repetition)
    df.loc[rep_mask, "fake_score"] += 0.25
    for idx in df.index[rep_mask]:
        df.at[idx, "fake_reasons"].append("Repetitive content")

    # Clip score to [0, 1]
    df["fake_score"] = df["fake_score"].clip(0, 1).round(3)

    return df


def get_suspicious_reviews(df: pd.DataFrame, threshold: float = 0.3, max_count: int = 50) -> list[dict]:
    suspicious = df[df["fake_score"] >= threshold].nlargest(max_count, "fake_score")
    results = []
    for idx, row in suspicious.iterrows():
        results.append({
            "index": int(idx),
            "text": row["review_text"][:300],
            "rating": int(row["rating"]),
            "fake_score": float(row["fake_score"]),
            "reasons": row["fake_reasons"],
        })
    return results
