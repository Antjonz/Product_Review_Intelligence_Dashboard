"""Generate a synthetic sample dataset with realistic product-specific reviews."""
import csv
import random
import os

random.seed(42)

# ── Product catalog ──────────────────────────────────────────────────────────

PRODUCTS = {
    "Sony WH-1000XM5 Headphones": {
        "id": "B0BX2L8PBT",
        "category": "headphones",
        "positive": [
            "The noise cancellation on these Sony headphones is phenomenal. I wear them on flights and can't hear the engine at all.",
            "Incredibly comfortable headphones. I wear them for 8-hour work sessions without any ear fatigue.",
            "Sound quality is outstanding. The bass is deep and mids are crystal clear. Best headphones I've owned.",
            "Battery life is amazing, easily lasts 30+ hours on a single charge.",
            "The multipoint Bluetooth connection works flawlessly between my laptop and phone.",
            "Very lightweight for over-ear headphones. Barely notice I'm wearing them.",
            "The adaptive sound control is a game changer. It adjusts ANC based on what I'm doing.",
            "Call quality is surprisingly good. My coworkers say I sound clear on Zoom meetings.",
        ],
        "negative": [
            "For $350 these headphones should sound better. My $150 pair had more detail.",
            "The touch controls on the ear cups are way too sensitive. I keep accidentally skipping tracks.",
            "Headband started cracking after 6 months. Build quality doesn't match the price.",
            "They get uncomfortably warm after about an hour. Not great for long listening sessions.",
            "Wind noise is terrible when walking outside. ANC can't handle it.",
        ],
    },
    "Apple AirPods Pro 2": {
        "id": "B0D1XD1ZV3",
        "category": "headphones",
        "positive": [
            "The AirPods Pro 2 transparency mode is insanely natural. It's like not wearing earbuds at all.",
            "Seamless integration with my iPhone and MacBook. The automatic switching is flawless.",
            "Active noise cancellation is impressive for such small earbuds.",
            "The spatial audio with head tracking makes movies feel like a theater experience.",
            "Charging case with the speaker is great for finding it when I inevitably lose it.",
            "USB-C finally! No more carrying a separate Lightning cable.",
        ],
        "negative": [
            "Ear tips don't stay in my ears during runs. Tried all three sizes.",
            "Battery life is only about 5 hours with ANC on. Not enough for long flights.",
            "The price keeps going up but the improvements are incremental at best.",
            "Sound quality is good but not audiophile level. Overrated for the price.",
        ],
    },
    "Samsung Galaxy S24 Ultra": {
        "id": "B0CS5HYQGF",
        "category": "phone",
        "positive": [
            "The Galaxy S24 Ultra camera is insane. 200MP main sensor takes incredibly detailed photos.",
            "Love the built-in S Pen. Perfect for quick notes and sketching ideas.",
            "The titanium frame feels incredibly premium. Best build quality on any phone.",
            "AI features like Circle to Search and Live Translate are genuinely useful daily.",
            "Display is stunning. The 2600 nit brightness makes it perfectly visible in direct sunlight.",
            "Seven years of software updates gives me confidence this phone will last.",
            "Battery easily lasts a full day of heavy use including gaming and camera.",
        ],
        "negative": [
            "This phone is way too heavy at 233g. My wrist gets tired holding it.",
            "Samsung's bloatware is ridiculous. So many preinstalled apps I can't remove.",
            "The curved edges cause accidental touches constantly. Very frustrating.",
            "Charging speed is still only 45W. Chinese phones are at 100W+ already.",
            "$1300 is absurd for a phone. The price increases every year.",
        ],
    },
    "Anker PowerCore 26800 Power Bank": {
        "id": "B01JIWQPMW",
        "category": "charger",
        "positive": [
            "This Anker power bank charges my phone 6+ times. Perfect for camping trips.",
            "Dual USB ports let me charge my phone and tablet simultaneously.",
            "Build quality is solid. Dropped it several times and it still works perfectly.",
            "The LED indicators clearly show remaining battery level.",
            "Charges surprisingly fast for such a large capacity battery bank.",
        ],
        "negative": [
            "This power bank is a brick. Way too heavy to carry in a pocket.",
            "Takes over 8 hours to fully recharge. That's painfully slow.",
            "No USB-C port. In 2024 that's unacceptable for a charger.",
            "It's not allowed on some airlines due to capacity. Found out the hard way.",
        ],
    },
    "Logitech MX Master 3S Mouse": {
        "id": "B09HM94VDS",
        "category": "mouse",
        "positive": [
            "The MX Master 3S scroll wheel is buttery smooth. The electromagnetic free-spinning is addictive.",
            "Ergonomic shape fits my hand perfectly. No more wrist pain after long work days.",
            "Connecting to three devices and switching with a button is incredibly convenient.",
            "The quiet clicks are perfect for late night work without disturbing anyone.",
            "Works on literally any surface including glass. The sensor is incredible.",
            "Customizable buttons with Logi Options+ make my workflow so much faster.",
        ],
        "negative": [
            "At $100 for a mouse, this is overpriced. Good but not $100 good.",
            "The thumb button placement causes accidental clicks when gripping normally.",
            "Bluetooth connection drops randomly on my Windows PC. Have to reconnect constantly.",
            "Not great for gaming. The sensor is fine for productivity but too slow for FPS games.",
        ],
    },
    "Kindle Paperwhite (2024)": {
        "id": "B0CFPJYX7P",
        "category": "tablet",
        "positive": [
            "The Kindle Paperwhite display is incredible. Reads just like real paper even in sunlight.",
            "Battery lasts weeks on a single charge. I only charge it once a month.",
            "The warm light adjustment is perfect for reading at night without straining my eyes.",
            "Waterproof design means I can read in the bath without worry. Game changer.",
            "Storage is more than enough. I have hundreds of books downloaded.",
            "Page turns are noticeably faster than the previous generation.",
        ],
        "negative": [
            "The Kindle ecosystem locks you into Amazon. Can't easily use other ebook stores.",
            "No audiobook playback through the speaker. Have to use Bluetooth which is clunky.",
            "Ads on the lock screen are annoying. Having to pay $20 extra to remove them is greedy.",
            "The cold white color option looks cheap compared to the black version.",
        ],
    },
    "JBL Flip 6 Bluetooth Speaker": {
        "id": "B09GYRYMQ3",
        "category": "speaker",
        "positive": [
            "This JBL speaker packs incredible volume for its size. Fills my entire backyard with sound.",
            "IP67 waterproof rating means I bring it to the pool and beach without worry.",
            "Bass is punchy and rich. Way better than expected from a portable speaker.",
            "Battery lasts 12 hours easily. Took it on a weekend camping trip with no issues.",
            "PartyBoost lets me connect two JBL speakers for stereo sound. Awesome feature.",
            "The rugged build has survived multiple drops onto concrete. Practically indestructible.",
        ],
        "negative": [
            "No 3.5mm aux input. If your phone dies you can't play music at all.",
            "No built-in microphone. Can't use it for speakerphone calls.",
            "The sound profile is very bass-heavy. Mids and highs get drowned out at high volume.",
            "No WiFi or smart assistant support. It's just a dumb Bluetooth speaker.",
        ],
    },
    "Nintendo Switch OLED": {
        "id": "B098RKWHHZ",
        "category": "console",
        "positive": [
            "The OLED screen on the Nintendo Switch is gorgeous. Games look so much better than the LCD model.",
            "The improved kickstand actually works now. Tabletop mode is finally usable.",
            "Zelda Tears of the Kingdom on this screen is a breathtaking experience.",
            "Great for travel. My kids stayed entertained on a 5 hour flight.",
            "The game library is massive. Between first party Nintendo titles and indie games there's always something to play.",
            "Local multiplayer with Joy-Cons is still the best couch gaming experience.",
        ],
        "negative": [
            "Joy-Con drift is still a problem. My left stick started drifting after 8 months.",
            "The hardware is showing its age. Games like Pokemon Scarlet run at terrible framerates.",
            "Charging $350 for what is essentially the same console with a better screen is a ripoff.",
            "Online service is still terrible compared to Xbox and PlayStation.",
            "No Bluetooth audio support without a dongle. How is this still missing?",
        ],
    },
}

NEUTRAL_TEMPLATES = [
    "It's okay. Nothing special but gets the job done for the price.",
    "Average product. Some features are great, others are disappointing.",
    "Works as described. Not amazing but not terrible either.",
    "Decent for the price. You get what you pay for with this one.",
    "Mixed feelings. The {feature} is nice but {issue} is mediocre.",
]

NEUTRAL_FEATURES = ["design", "build quality", "battery life", "performance"]
NEUTRAL_ISSUES = ["the software", "the price", "customer support", "durability"]

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


def generate_date():
    year = random.choice([2023, 2024])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def vary_text(text: str) -> str:
    prefixes = ["", "Overall, ", "Honestly, ", "I think ", "In my opinion, ", ""]
    suffixes = [
        "", "", "", "", "", "",
    ]
    return random.choice(prefixes) + text + random.choice(suffixes)


def main():
    rows = []

    for product_name, info in PRODUCTS.items():
        pid = info["id"]

        # Positive reviews
        for _ in range(60):
            text = vary_text(random.choice(info["positive"]))
            rating = random.choice([4, 4, 5, 5, 5])
            rows.append((text, rating, generate_date(), pid, product_name))

        # Negative reviews
        for _ in range(30):
            text = vary_text(random.choice(info["negative"]))
            rating = random.choice([1, 1, 2, 2])
            rows.append((text, rating, generate_date(), pid, product_name))

        # Neutral reviews
        for _ in range(15):
            template = random.choice(NEUTRAL_TEMPLATES)
            text = template.format(
                feature=random.choice(NEUTRAL_FEATURES),
                issue=random.choice(NEUTRAL_ISSUES),
            )
            text = vary_text(text)
            rating = 3
            rows.append((text, rating, generate_date(), pid, product_name))

    # Fake positive reviews spread across products
    for _ in range(30):
        text = random.choice(FAKE_POSITIVE)
        rating = 5
        info = random.choice(list(PRODUCTS.values()))
        name = [k for k, v in PRODUCTS.items() if v is info][0]
        rows.append((text, rating, generate_date(), info["id"], name))

    # Mismatched reviews (negative text, 5 stars)
    for _ in range(20):
        text = random.choice(FAKE_NEGATIVE_TEXT_HIGH_RATING)
        rating = 5
        info = random.choice(list(PRODUCTS.values()))
        name = [k for k, v in PRODUCTS.items() if v is info][0]
        rows.append((text, rating, generate_date(), info["id"], name))

    random.shuffle(rows)

    out_path = os.path.join(os.path.dirname(__file__), "sample_data", "amazon_reviews.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["review_text", "rating", "date", "product_id", "product_name"])
        for row in rows:
            writer.writerow(row)

    print(f"Generated {len(rows)} reviews -> {out_path}")


if __name__ == "__main__":
    main()
