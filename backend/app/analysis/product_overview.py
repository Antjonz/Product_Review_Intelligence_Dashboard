"""Detect what products reviews are about and generate a natural language overview."""
from collections import Counter
import re
import pandas as pd

from ..utils.data_processing import tokenize, STOP_WORDS

# Common non-product words to exclude from product detection
NON_PRODUCT_WORDS = STOP_WORDS | {
    "product", "item", "purchase", "bought", "buy", "thing", "stuff",
    "one", "use", "used", "using", "work", "works", "working", "worked",
    "great", "good", "bad", "best", "worst", "love", "hate", "nice",
    "amazing", "terrible", "awesome", "awful", "perfect", "horrible",
    "excellent", "poor", "fantastic", "disappointed", "happy", "recommend",
    "money", "price", "quality", "time", "day", "week", "month", "year",
    "first", "last", "new", "old", "highly", "definitely", "absolutely",
    "really", "very", "pretty", "quite", "ever", "never", "always",
    "everything", "nothing", "something", "anything",
}

# Known product category keywords
PRODUCT_CATEGORIES = {
    "headphones": ["headphone", "headphones", "earbuds", "earphone", "earbud", "ear"],
    "speaker": ["speaker", "speakers", "soundbar", "subwoofer", "bluetooth speaker"],
    "phone": ["phone", "smartphone", "iphone", "android", "samsung", "pixel", "mobile"],
    "laptop": ["laptop", "notebook", "macbook", "chromebook", "ultrabook"],
    "tablet": ["tablet", "ipad", "kindle", "e-reader"],
    "camera": ["camera", "dslr", "mirrorless", "webcam", "gopro", "lens"],
    "tv": ["tv", "television", "monitor", "display", "screen", "oled", "led"],
    "keyboard": ["keyboard", "mechanical keyboard", "keycap", "keyswitch"],
    "mouse": ["mouse", "trackpad", "touchpad", "gaming mouse"],
    "charger": ["charger", "charging", "cable", "usb", "adapter", "power bank"],
    "watch": ["watch", "smartwatch", "fitness tracker", "fitbit", "garmin"],
    "router": ["router", "wifi", "modem", "mesh", "ethernet", "networking"],
    "printer": ["printer", "scanner", "ink", "toner", "printing"],
    "console": ["console", "playstation", "xbox", "nintendo", "switch", "gaming"],
    "appliance": ["blender", "toaster", "microwave", "vacuum", "air fryer", "coffee maker"],
}


def detect_products(df: pd.DataFrame) -> list[dict]:
    """Try to identify what products the reviews are about."""
    all_text = " ".join(df["review_text"].str.lower().tolist())

    # 1. Check if product_id column exists and has useful values
    product_names = []
    if "product_id" in df.columns:
        top_products = df["product_id"].value_counts().head(10)
        for pid, count in top_products.items():
            product_names.append({
                "name": str(pid),
                "count": int(count),
                "type": "product_id",
            })

    # 2. Match against known product categories
    category_hits = {}
    for category, keywords in PRODUCT_CATEGORIES.items():
        count = 0
        for kw in keywords:
            count += len(re.findall(r"\b" + re.escape(kw) + r"\b", all_text))
        if count > 0:
            category_hits[category] = count

    detected_categories = sorted(category_hits.items(), key=lambda x: -x[1])[:5]

    # 3. Extract frequently mentioned nouns/noun-like words (bigrams)
    words = re.findall(r"\b[a-z]{3,}\b", all_text)
    word_freq = Counter(w for w in words if w not in NON_PRODUCT_WORDS)

    # Bigrams for compound product names
    bigrams = []
    for i in range(len(words) - 1):
        if words[i] not in NON_PRODUCT_WORDS and words[i + 1] not in NON_PRODUCT_WORDS:
            bigrams.append(f"{words[i]} {words[i+1]}")
    bigram_freq = Counter(bigrams)

    top_terms = [w for w, _ in word_freq.most_common(15)]
    top_bigrams = [b for b, c in bigram_freq.most_common(10) if c >= 3]

    return {
        "product_ids": product_names[:10],
        "detected_categories": [
            {"category": cat.title(), "mentions": cnt}
            for cat, cnt in detected_categories
        ],
        "key_terms": top_terms,
        "key_phrases": top_bigrams,
    }


def generate_overview_summary(df: pd.DataFrame, product_info: dict, insights: dict) -> dict:
    """Generate a natural language AI overview from the analysis data."""
    total = len(df)
    avg_rating = float(df["rating"].mean())
    sentiment_counts = df["sentiment"].value_counts()
    pos_pct = round(sentiment_counts.get("positive", 0) / total * 100, 1)
    neg_pct = round(sentiment_counts.get("negative", 0) / total * 100, 1)
    neu_pct = round(sentiment_counts.get("neutral", 0) / total * 100, 1)

    # Determine what the reviews are about
    product_desc = _describe_products(product_info)

    # Rating summary
    rating_dist = df["rating"].value_counts().sort_index()
    five_star_pct = round(rating_dist.get(5, 0) / total * 100, 1)
    one_star_pct = round(rating_dist.get(1, 0) / total * 100, 1)

    # What people like
    praises = insights.get("praises", [])
    praise_items = [p["text"] for p in praises[:5]]

    # What people dislike
    complaints = insights.get("complaints", [])
    complaint_items = [c["text"] for c in complaints[:5]]

    # Build summary paragraphs
    product_line = f"These reviews are about {product_desc}." if product_desc else "Product category could not be determined from the review text."

    if avg_rating >= 4.0:
        overall_sentiment = "overwhelmingly positive"
    elif avg_rating >= 3.5:
        overall_sentiment = "generally positive"
    elif avg_rating >= 2.5:
        overall_sentiment = "mixed"
    elif avg_rating >= 2.0:
        overall_sentiment = "generally negative"
    else:
        overall_sentiment = "overwhelmingly negative"

    overview_para = (
        f"Based on {total:,} reviews, customer sentiment is {overall_sentiment} "
        f"with an average rating of {avg_rating:.1f}/5. "
        f"{pos_pct}% of reviews are positive, {neg_pct}% are negative, and {neu_pct}% are neutral. "
        f"{five_star_pct}% of customers gave 5 stars, while {one_star_pct}% gave 1 star."
    )

    likes_para = ""
    if praise_items:
        likes_para = "Customers frequently praise: " + _join_list(praise_items[:5]) + "."

    dislikes_para = ""
    if complaint_items:
        dislikes_para = "Common complaints include: " + _join_list(complaint_items[:5]) + "."

    # Recommendation
    if avg_rating >= 4.0:
        rec = "The majority of customers are satisfied and would likely recommend this product."
    elif avg_rating >= 3.0:
        rec = "Customer opinions are divided. The product works well for some but has notable issues for others."
    else:
        rec = "Most customers are dissatisfied. Significant improvements appear needed based on recurring complaints."

    return {
        "product_description": product_line,
        "overall_summary": overview_para,
        "what_people_like": likes_para,
        "what_people_dislike": dislikes_para,
        "recommendation": rec,
    }


def _describe_products(product_info: dict) -> str:
    """Build a natural language description of what products the reviews cover."""
    parts = []

    categories = product_info.get("detected_categories", [])
    if categories:
        cat_names = [c["category"].lower() for c in categories[:3]]
        if len(cat_names) == 1:
            parts.append(cat_names[0] + " products")
        else:
            parts.append(", ".join(cat_names[:-1]) + " and " + cat_names[-1] + " products")

    product_ids = product_info.get("product_ids", [])
    if product_ids and not categories:
        count = len(product_ids)
        parts.append(f"{count} different product{'s' if count > 1 else ''}")

    key_terms = product_info.get("key_terms", [])
    if not parts and key_terms:
        parts.append("products related to " + ", ".join(key_terms[:3]))

    return " — specifically ".join(parts) if parts else ""


def _join_list(items: list[str]) -> str:
    if len(items) == 0:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + ", and " + items[-1]
