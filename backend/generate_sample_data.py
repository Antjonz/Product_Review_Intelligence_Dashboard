"""Generate a synthetic sample dataset for development/demo purposes."""
import csv
import random
import os

random.seed(42)

POSITIVE_TEMPLATES = [
    "Absolutely love this product! The quality is outstanding and it works perfectly.",
    "Great value for the money. Exceeded my expectations in every way.",
    "Best purchase I've made this year. Highly recommend to everyone.",
    "The build quality is fantastic. Very durable and well-made product.",
    "Easy to set up and use right out of the box. Intuitive design.",
    "Sound quality is amazing for this price range. Crystal clear audio.",
    "Battery life is incredible, lasts all day with heavy use.",
    "Perfect fit and very comfortable to wear for long periods.",
    "Fast shipping and the product arrived in perfect condition.",
    "Customer support was extremely helpful when I had questions.",
    "This exceeded all my expectations. The performance is top-notch.",
    "Sleek design and very lightweight. Perfect for travel.",
    "The display is gorgeous with vibrant colors and sharp text.",
    "Works seamlessly with all my devices. Great compatibility.",
    "Solid construction, feels premium. Worth every penny.",
    "Very impressed with the features at this price point.",
    "The noise cancellation is phenomenal. Blocks out everything.",
    "Setup took less than 5 minutes. Very user-friendly.",
    "Love the compact size. Doesn't take up much space at all.",
    "Excellent product, bought a second one for my office.",
]

NEGATIVE_TEMPLATES = [
    "Terrible quality. Broke after just two weeks of normal use.",
    "Worst purchase ever. Does not work as advertised at all.",
    "Very disappointed. The product feels cheap and flimsy.",
    "Battery barely lasts 2 hours. Complete waste of money.",
    "Customer service was unhelpful and rude when I called.",
    "The sound quality is awful. Tinny and distorted at any volume.",
    "Stopped working after one month. No response from warranty.",
    "Way too expensive for what you get. Total ripoff.",
    "The software is buggy and crashes constantly.",
    "Arrived damaged and the return process was a nightmare.",
    "Very uncomfortable to use. Gave me headaches after 30 minutes.",
    "The screen is dim and colors look washed out.",
    "Does not fit properly despite following the size guide.",
    "Extremely slow performance. Freezes during basic tasks.",
    "Made a lot of noise and overheated quickly.",
]

NEUTRAL_TEMPLATES = [
    "It's okay. Nothing special but gets the job done.",
    "Average product. Some good features, some not so great.",
    "Works as described. Not amazing but not terrible either.",
    "Decent for the price. You get what you pay for.",
    "Mixed feelings. The design is nice but performance is mediocre.",
]

FAKE_POSITIVE = [
    "AMAZING AMAZING AMAZING BEST PRODUCT EVER BUY NOW!!!",
    "good good good good good good product good good",
    "Five stars.",
    "Best",
    "Perfect perfect perfect love it so much best ever!!!!",
    "great",
    "BUY THIS RIGHT NOW YOU WONT REGRET IT BEST THING EVER MADE",
]

FAKE_NEGATIVE_TEXT_HIGH_RATING = [
    "Terrible product, broke immediately, waste of money, DO NOT BUY.",
    "Awful quality, horrible experience, never buying again.",
    "This is garbage. Complete junk. Worst thing I ever purchased.",
]

PRODUCT_IDS = [f"PROD-{i:04d}" for i in range(1, 21)]


def generate_date():
    year = random.choice([2023, 2024])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def vary_text(text: str) -> str:
    """Add slight variation to template text."""
    prefixes = ["", "Overall, ", "Honestly, ", "I think ", "In my opinion, ", ""]
    suffixes = [
        "", " Would buy again.", " Not sure about it.", "",
        " Time will tell.", " We'll see how it holds up.", "",
    ]
    return random.choice(prefixes) + text + random.choice(suffixes)


def main():
    rows = []

    # ~500 positive reviews (ratings 4-5)
    for _ in range(500):
        text = vary_text(random.choice(POSITIVE_TEMPLATES))
        rating = random.choice([4, 4, 5, 5, 5])
        rows.append((text, rating, generate_date(), random.choice(PRODUCT_IDS)))

    # ~300 negative reviews (ratings 1-2)
    for _ in range(300):
        text = vary_text(random.choice(NEGATIVE_TEMPLATES))
        rating = random.choice([1, 1, 2, 2])
        rows.append((text, rating, generate_date(), random.choice(PRODUCT_IDS)))

    # ~150 neutral reviews (rating 3)
    for _ in range(150):
        text = vary_text(random.choice(NEUTRAL_TEMPLATES))
        rating = 3
        rows.append((text, rating, generate_date(), random.choice(PRODUCT_IDS)))

    # ~30 obviously fake positive reviews (rating 5)
    for _ in range(30):
        text = random.choice(FAKE_POSITIVE)
        rating = 5
        rows.append((text, rating, generate_date(), random.choice(PRODUCT_IDS)))

    # ~20 mismatched reviews (negative text, 5-star rating = suspicious)
    for _ in range(20):
        text = random.choice(FAKE_NEGATIVE_TEXT_HIGH_RATING)
        rating = 5
        rows.append((text, rating, generate_date(), random.choice(PRODUCT_IDS)))

    random.shuffle(rows)

    out_path = os.path.join(os.path.dirname(__file__), "sample_data", "amazon_reviews.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["review_text", "rating", "date", "product_id"])
        for row in rows:
            writer.writerow(row)

    print(f"Generated {len(rows)} reviews -> {out_path}")


if __name__ == "__main__":
    main()
