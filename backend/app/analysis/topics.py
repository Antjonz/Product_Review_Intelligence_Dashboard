import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

from ..utils.data_processing import tokenize


TOPIC_LABELS = {
    "quality": ["quality", "build", "material", "durable", "cheap", "solid", "broke", "flimsy"],
    "value": ["price", "value", "money", "worth", "expensive", "affordable", "cost", "deal"],
    "usability": ["easy", "use", "simple", "complicated", "difficult", "intuitive", "setup", "install"],
    "performance": ["fast", "slow", "performance", "speed", "powerful", "lag", "smooth", "efficient"],
    "design": ["design", "look", "style", "color", "size", "sleek", "compact", "aesthetic"],
    "service": ["service", "support", "customer", "shipping", "delivery", "return", "warranty", "refund"],
    "battery": ["battery", "charge", "life", "power", "last", "drain", "hours"],
    "sound": ["sound", "audio", "volume", "bass", "noise", "speaker", "loud", "quiet"],
    "display": ["screen", "display", "resolution", "bright", "clear", "pixel", "hd"],
    "comfort": ["comfortable", "fit", "wear", "soft", "light", "heavy", "ergonomic"],
}


def _label_topic(keywords: list[str]) -> str:
    best_label = "general"
    best_score = 0
    for label, label_words in TOPIC_LABELS.items():
        score = sum(1 for kw in keywords if kw in label_words)
        if score > best_score:
            best_score = score
            best_label = label
    return best_label


def extract_topics(texts: list[str], n_topics: int = 6, n_words: int = 8) -> list[dict]:
    if len(texts) < 10:
        return []

    vectorizer = CountVectorizer(
        max_df=0.9, min_df=max(2, len(texts) // 100),
        max_features=2000, stop_words="english"
    )
    try:
        doc_term = vectorizer.fit_transform(texts)
    except ValueError:
        return []

    lda = LatentDirichletAllocation(
        n_components=min(n_topics, len(texts) // 5),
        random_state=42, max_iter=20, learning_method="online"
    )
    lda.fit(doc_term)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for idx, component in enumerate(lda.components_):
        top_indices = component.argsort()[-n_words:][::-1]
        keywords = [feature_names[i] for i in top_indices]
        label = _label_topic(keywords)
        topics.append({
            "name": label.title(),
            "keywords": keywords,
            "count": int(component.sum()),
            "weight": round(float(component.sum() / lda.components_.sum()), 3),
        })
    return topics


def get_word_frequencies(texts: list[str], top_n: int = 40) -> list[dict]:
    all_tokens = []
    for t in texts:
        all_tokens.extend(tokenize(t))
    counter = Counter(all_tokens)
    return [{"word": w, "count": c} for w, c in counter.most_common(top_n)]


def extract_topics_by_sentiment(df) -> dict:
    positive = df[df["sentiment"] == "positive"]["review_text"].tolist()
    negative = df[df["sentiment"] == "negative"]["review_text"].tolist()
    return {
        "positive": extract_topics(positive, n_topics=4),
        "negative": extract_topics(negative, n_topics=4),
    }


def get_word_frequencies_by_sentiment(df) -> dict:
    positive = df[df["sentiment"] == "positive"]["review_text"].tolist()
    negative = df[df["sentiment"] == "negative"]["review_text"].tolist()
    return {
        "positive": get_word_frequencies(positive),
        "negative": get_word_frequencies(negative),
    }
