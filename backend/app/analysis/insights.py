"""Extract meaningful key insights using TF-IDF on bigrams/trigrams."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter


# Generic phrases to filter out — these score high in TF-IDF but aren't useful insights
STOP_PHRASES = {
    "the product", "this product", "this item", "the item",
    "bought this", "buy this", "bought it", "got this",
    "would recommend", "don recommend", "ve been", "ve had",
    "ve ever", "it was", "it is", "this is", "that is",
    "in my", "on the", "of the", "for the", "to the",
    "and the", "and it", "but the", "but it", "with the",
    "my opinion", "think this", "opinion this",
    "overall this", "honestly this", "in opinion",
    "time will", "will tell", "we ll", "ll see",
    "would buy", "buy again", "not sure",
    "average product", "average product good", "decent price",
    "good features", "good features great", "product good features",
    "product good", "not amazing", "not terrible",
    "gets job done", "nothing special", "pay get",
    "features great", "great not", "not great", "product feels",
    "30 minutes", "minutes", "ve year", "purchase ve",
    "ve made", "ve bought", "ve seen", "ve used",
}

# Words that are too generic on their own to form a useful phrase
FILLER_WORDS = {
    "honestly", "overall", "opinion", "think", "really", "pretty",
    "quite", "just", "also", "got", "lot", "bit", "way",
}


def _extract_distinctive_phrases(
    target_texts: list[str],
    contrast_texts: list[str],
    n: int = 8,
) -> list[dict]:
    """
    Extract phrases distinctive to target_texts vs contrast_texts.

    Uses TF-IDF on bigrams/trigrams. Scores each phrase by how much more
    important it is in the target group compared to the contrast group.
    """
    if len(target_texts) < 5:
        return []

    all_texts = target_texts + contrast_texts
    labels = [1] * len(target_texts) + [0] * len(contrast_texts)

    vectorizer = TfidfVectorizer(
        ngram_range=(2, 3),
        max_features=5000,
        min_df=max(2, len(target_texts) // 50),
        max_df=0.8,
        stop_words="english",
        sublinear_tf=True,
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
    except ValueError:
        return []

    feature_names = vectorizer.get_feature_names_out()

    # Average TF-IDF score for target vs contrast groups
    target_mask = np.array(labels) == 1
    contrast_mask = ~target_mask

    target_mean = np.asarray(tfidf_matrix[target_mask].mean(axis=0)).flatten()
    if contrast_mask.any():
        contrast_mean = np.asarray(tfidf_matrix[contrast_mask].mean(axis=0)).flatten()
    else:
        contrast_mean = np.zeros_like(target_mean)

    # Distinctiveness = target score - contrast score
    # Phrases that appear a lot in target but not in contrast rank highest
    distinctiveness = target_mean - contrast_mean

    # Also need raw count in target for the "count" field
    target_doc_freq = np.asarray((tfidf_matrix[target_mask] > 0).sum(axis=0)).flatten()

    # Rank by distinctiveness
    top_indices = distinctiveness.argsort()[::-1]

    results = []
    used_words = set()  # track word overlap to avoid near-duplicate phrases

    for idx in top_indices:
        if len(results) >= n:
            break

        phrase = feature_names[idx]
        count = int(target_doc_freq[idx])

        # Skip generic phrases
        if phrase in STOP_PHRASES:
            continue
        # Skip if barely mentioned
        if count < 2:
            continue

        words_list = phrase.split()
        words = set(words_list)

        # Skip phrases with duplicate words (e.g., "good good")
        if len(words) < len(words_list):
            continue

        # Skip if mostly filler words
        meaningful = words - FILLER_WORDS
        if len(meaningful) < max(1, len(words) - 1):
            continue

        # Skip phrases containing very short tokens (contraction artifacts like "ve", "ll", "re")
        if any(len(w) < 3 for w in words_list):
            continue

        # Skip if too much overlap with already-selected phrases
        # (this prevents "comfortable wear", "wear long", "comfortable wear long" all appearing)
        overlap = words & used_words
        if len(overlap) > 0 and len(overlap) >= len(words) - 1:
            continue

        used_words.update(words)
        results.append({
            "text": phrase,
            "count": count,
        })

    return results


def extract_key_insights(positive_df, negative_df, n=8) -> dict:
    """Extract meaningful praise and complaint phrases from reviews using TF-IDF.

    Uses sentiment_score to filter more strictly:
    - Praises come from clearly positive reviews (score > 0.3)
    - Complaints come from clearly negative reviews (score < -0.3)
    This avoids neutral reviews bleeding into either group.
    """
    if "sentiment_score" in positive_df.columns:
        pos_texts = positive_df[positive_df["sentiment_score"] > 0.3]["review_text"].tolist()
    else:
        pos_texts = positive_df["review_text"].tolist()
    if "sentiment_score" in negative_df.columns:
        neg_texts = negative_df[negative_df["sentiment_score"] < -0.3]["review_text"].tolist()
    else:
        neg_texts = negative_df["review_text"].tolist()

    praises = _extract_distinctive_phrases(pos_texts, neg_texts, n=n)
    for p in praises:
        p["sentiment"] = "positive"

    complaints = _extract_distinctive_phrases(neg_texts, pos_texts, n=n)
    for c in complaints:
        c["sentiment"] = "negative"

    return {"praises": praises, "complaints": complaints}
