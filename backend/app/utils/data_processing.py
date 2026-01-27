import re
import pandas as pd
import numpy as np


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now", "d",
    "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn", "didn",
    "doesn", "hadn", "hasn", "haven", "isn", "ma", "mightn", "mustn",
    "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn",
    "also", "would", "could", "one", "two", "get", "got", "really",
    "much", "even", "like", "well", "still", "back", "going", "went",
}


def tokenize(text: str) -> list[str]:
    words = clean_text(text).split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Map common column name variants
    col_map = {}
    for c in df.columns:
        if "review" in c and ("text" in c or "body" in c or "content" in c):
            col_map[c] = "review_text"
        elif c in ("reviewtext", "comment", "comments", "feedback", "text"):
            col_map[c] = "review_text"
        elif c in ("star", "stars", "score", "star_rating", "overall"):
            col_map[c] = "rating"
        elif "date" in c or "time" in c:
            col_map[c] = "date"
        elif "product" in c and "id" in c:
            col_map[c] = "product_id"
    df.rename(columns=col_map, inplace=True)

    if "review_text" not in df.columns:
        raise ValueError(
            "CSV must contain a review text column. "
            "Expected one of: review_text, reviewText, comment, text, feedback"
        )
    if "rating" not in df.columns:
        raise ValueError(
            "CSV must contain a rating column. "
            "Expected one of: rating, star, stars, score, overall"
        )

    df["review_text"] = df["review_text"].astype(str).fillna("")
    df = df[df["review_text"].str.strip().str.len() > 0].copy()

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df.dropna(subset=["rating"], inplace=True)
    df["rating"] = df["rating"].astype(int).clip(1, 5)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df.reset_index(drop=True, inplace=True)
    return df
