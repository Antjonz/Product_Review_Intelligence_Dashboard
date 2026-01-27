"""Extract meaningful key insights (praises and complaints) from reviews."""
import re
from collections import Counter

# Phrases that indicate specific praise or complaint topics.
# We match these against lowercased review text.
PRAISE_PATTERNS = [
    (r"\b(?:great|excellent|good|amazing|fantastic|superb|outstanding) (?:quality|build quality)\b", "great quality"),
    (r"\b(?:great|excellent|good|amazing|best|fantastic) value\b", "great value for money"),
    (r"\bworth (?:every|the) (?:penny|money|price)\b", "worth the price"),
    (r"\beasy to (?:set up|setup|use|install|assemble)\b", "easy to set up and use"),
    (r"\b(?:battery|charge) (?:lasts?|life is) (?:all day|incredible|amazing|great|long|forever)\b", "excellent battery life"),
    (r"\bbattery life is (?:incredible|amazing|great|excellent|fantastic)\b", "excellent battery life"),
    (r"\b(?:sound|audio) (?:quality )?is (?:amazing|great|excellent|fantastic|superb|awesome|clear|crisp)\b", "great sound quality"),
    (r"\bcrystal clear (?:audio|sound)\b", "great sound quality"),
    (r"\b(?:very |super )?(?:comfortable|comfy) to (?:wear|use)\b", "comfortable to wear"),
    (r"\b(?:perfect|great|nice|good) fit\b", "comfortable fit"),
    (r"\b(?:looks? (?:great|amazing|sleek|premium|beautiful)|sleek design|beautiful design)\b", "sleek design"),
    (r"\b(?:fast|quick) shipping\b", "fast shipping"),
    (r"\barrived (?:in )?perfect (?:condition)?\b", "arrived in perfect condition"),
    (r"\b(?:customer )?(?:support|service) was (?:extremely |very )?helpful\b", "helpful customer support"),
    (r"\b(?:highly|would|definitely) recommend\b", "highly recommended"),
    (r"\bexceeded (?:my |all )?expectations\b", "exceeded expectations"),
    (r"\b(?:very |super )?(?:durable|well[- ]made|solid|sturdy)\b", "durable and well-made"),
    (r"\b(?:lightweight|light weight|very light)\b", "lightweight and portable"),
    (r"\bnoise cancell?ation is (?:phenomenal|great|amazing|excellent)\b", "great noise cancellation"),
    (r"\buser[- ]friendly\b", "user-friendly"),
    (r"\b(?:works? (?:perfectly|great|seamlessly|flawlessly))\b", "works perfectly"),
    (r"\b(?:love|loved) (?:this|the|it)\b", "customers love it"),
    (r"\bbest purchase\b", "considered a great purchase"),
    (r"\b(?:compact|small) size\b", "compact size"),
]

COMPLAINT_PATTERNS = [
    (r"\b(?:broke|broken|stopped working) (?:after|within|in)\b", "breaks easily"),
    (r"\b(?:cheap|flimsy|fragile|poor)(?:ly made| quality| build| material)?\b", "feels cheap and flimsy"),
    (r"\b(?:battery (?:barely|only|doesn.t) (?:lasts?|lasted?))\b", "poor battery life"),
    (r"\bbattery (?:life )?(?:is )?(?:terrible|awful|bad|short|poor)\b", "poor battery life"),
    (r"\bwaste of money\b", "waste of money"),
    (r"\b(?:not worth|overpriced|too expensive|total rip\s?off)\b", "overpriced"),
    (r"\b(?:customer )?(?:support|service) was (?:unhelpful|rude|terrible|awful|horrible|useless|unresponsive)\b", "poor customer service"),
    (r"\bno response from (?:warranty|support|customer)\b", "poor customer service"),
    (r"\b(?:sound|audio) (?:quality )?is (?:awful|terrible|bad|poor|tinny|distorted)\b", "poor sound quality"),
    (r"\btinny and distorted\b", "poor sound quality"),
    (r"\b(?:does not|doesn.t|did not|didn.t) work as (?:advertised|described|expected)\b", "does not work as advertised"),
    (r"\b(?:arrived damaged|came broken|received damaged)\b", "arrived damaged"),
    (r"\breturn (?:process|policy) was (?:a nightmare|terrible|difficult|horrible)\b", "difficult return process"),
    (r"\b(?:software|app) is (?:buggy|glitchy|crashes?|terrible)\b", "buggy software"),
    (r"\bcrashe?s? (?:constantly|frequently|often|a lot)\b", "crashes frequently"),
    (r"\b(?:very |super |extremely )?(?:uncomfortable|gives? me headaches?)\b", "uncomfortable to use"),
    (r"\b(?:screen|display) is (?:dim|dark|dull|terrible|bad)\b", "poor display quality"),
    (r"\bcolors? look (?:washed out|faded|bad|dull)\b", "poor display quality"),
    (r"\b(?:does not|doesn.t) fit\b", "poor fit"),
    (r"\b(?:extremely |very )?slow (?:performance)?\b", "slow performance"),
    (r"\b(?:freezes?|lags?|lagging) (?:during|constantly|a lot)\b", "slow performance"),
    (r"\b(?:over ?heated?|over ?heating|(?:made|makes) a lot of noise|too noisy|very loud)\b", "overheating or noisy"),
    (r"\bworst (?:purchase|product|buy)\b", "worst purchase"),
    (r"\b(?:never|don.t|do not) buy(?:ing)?\b", "customers warn against buying"),
]


def _count_pattern_matches(texts: list[str], patterns: list[tuple[str, str]]) -> list[dict]:
    """Count how many reviews match each pattern."""
    lower_texts = [t.lower() for t in texts]
    counts = Counter()
    for text in lower_texts:
        seen_labels = set()
        for pattern, label in patterns:
            if label not in seen_labels and re.search(pattern, text):
                counts[label] += 1
                seen_labels.add(label)
    return counts


def extract_key_insights(positive_df, negative_df, n=8) -> dict:
    """Extract meaningful praise and complaint phrases from reviews."""
    pos_texts = positive_df["review_text"].tolist()
    neg_texts = negative_df["review_text"].tolist()

    praise_counts = _count_pattern_matches(pos_texts, PRAISE_PATTERNS)
    complaint_counts = _count_pattern_matches(neg_texts, COMPLAINT_PATTERNS)

    praises = [
        {"text": label, "count": count, "sentiment": "positive"}
        for label, count in praise_counts.most_common(n)
        if count >= 2
    ]
    complaints = [
        {"text": label, "count": count, "sentiment": "negative"}
        for label, count in complaint_counts.most_common(n)
        if count >= 2
    ]

    return {"praises": praises, "complaints": complaints}
