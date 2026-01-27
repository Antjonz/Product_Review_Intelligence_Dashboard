"""Extract meaningful key insights using TF-IDF on bigrams/trigrams,
then map back to original review sentences for human-readable output."""
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# Generic n-grams to skip
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

FILLER_WORDS = {
    "honestly", "overall", "opinion", "think", "really", "pretty",
    "quite", "just", "also", "got", "lot", "bit", "way",
}


def _find_source_sentence(phrase_words: set[str], texts: list[str]) -> str | None:
    """Find the best original sentence containing all words of an n-gram phrase.

    Returns a clean, short sentence fragment from the actual review text.
    """
    best = None
    best_len = 999

    for text in texts:
        # Split review into sentences
        sentences = re.split(r"[.!?]+", text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 8:
                continue
            lower = sentence.lower()
            # Check if all key words from the n-gram appear in this sentence
            if all(w in lower for w in phrase_words):
                # Prefer shorter sentences (more focused)
                if len(sentence) < best_len:
                    best = sentence
                    best_len = len(sentence)
                    if best_len < 60:
                        # Short enough, stop searching
                        break
        if best and best_len < 60:
            break

    if best:
        # Clean up: strip leading filler, capitalize
        best = re.sub(r"^(?:honestly|overall|in my opinion|i think|i feel)\s*,?\s*", "", best, flags=re.IGNORECASE)
        best = best.strip()
        if best:
            best = best[0].upper() + best[1:]
            # Truncate if too long
            if len(best) > 80:
                best = best[:77].rsplit(" ", 1)[0] + "..."
    return best


def _extract_distinctive_phrases(
    target_texts: list[str],
    contrast_texts: list[str],
    n: int = 8,
) -> list[dict]:
    """Extract phrases distinctive to target_texts vs contrast_texts using TF-IDF,
    then map each phrase back to a readable source sentence."""
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

    target_mask = np.array(labels) == 1
    contrast_mask = ~target_mask

    target_mean = np.asarray(tfidf_matrix[target_mask].mean(axis=0)).flatten()
    if contrast_mask.any():
        contrast_mean = np.asarray(tfidf_matrix[contrast_mask].mean(axis=0)).flatten()
    else:
        contrast_mean = np.zeros_like(target_mean)

    distinctiveness = target_mean - contrast_mean
    target_doc_freq = np.asarray((tfidf_matrix[target_mask] > 0).sum(axis=0)).flatten()

    top_indices = distinctiveness.argsort()[::-1]

    # Phase 1: collect candidate n-gram phrases
    candidates = []
    used_words = set()

    for idx in top_indices:
        if len(candidates) >= n * 3:  # collect more candidates, will filter later
            break

        phrase = feature_names[idx]
        count = int(target_doc_freq[idx])

        if phrase in STOP_PHRASES or count < 2:
            continue

        words_list = phrase.split()
        words = set(words_list)

        if len(words) < len(words_list):
            continue
        meaningful = words - FILLER_WORDS
        if len(meaningful) < max(1, len(words) - 1):
            continue
        if any(len(w) < 3 for w in words_list):
            continue

        overlap = words & used_words
        if len(overlap) > 0 and len(overlap) >= len(words) - 1:
            continue

        used_words.update(words)
        candidates.append({"phrase_words": words, "count": count})

    # Phase 2: map each candidate back to a readable source sentence
    results = []
    used_sentences = set()

    for cand in candidates:
        if len(results) >= n:
            break

        sentence = _find_source_sentence(cand["phrase_words"], target_texts)
        if not sentence:
            continue

        # Deduplicate similar sentences
        key = sentence.lower()[:40]
        if key in used_sentences:
            continue
        used_sentences.add(key)

        results.append({
            "text": sentence,
            "count": cand["count"],
        })

    return results


def extract_key_insights(positive_df, negative_df, n=8) -> dict:
    """Extract human-readable praise and complaint phrases from reviews using TF-IDF."""
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
