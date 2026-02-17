import os
import json
import uuid
import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    UploadResponse, PredictRequest, PredictResponse,
    SampleDatasetInfo,
)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
from .utils.data_processing import preprocess_dataframe
from .analysis.sentiment import analyze_sentiments, build_sentiment_timeline, get_sentiment_breakdown
from .analysis.topics import extract_topics_by_sentiment, get_word_frequencies_by_sentiment
from .analysis.fake_detection import detect_fake_reviews, get_suspicious_reviews
from .analysis.predictions import predictor
from .analysis.product_overview import detect_products, generate_overview_summary

app = FastAPI(title="Product Review Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded dataframes
_uploads: dict[str, pd.DataFrame] = {}

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")

# Health check endpoint
@app.get("/api/health")
def health():
    return {"status": "ok"}

# File upload endpoint with validation and preprocessing
@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")

    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(400, f"Failed to parse CSV: {e}")

    try:
        df = preprocess_dataframe(df)
    except ValueError as e:
        raise HTTPException(400, str(e))

    file_id = str(uuid.uuid4())
    _uploads[file_id] = df

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        total_rows=len(df),
        columns=list(df.columns),
        message="File uploaded and validated successfully",
    )

# Analysis endpoint that performs all analyses and returns a comprehensive report
@app.post("/api/analyze")
async def analyze(file_id: str):
    if file_id not in _uploads:
        raise HTTPException(404, "File not found. Please upload again.")

    df = _uploads[file_id]

    # Sentiment analysis
    df = analyze_sentiments(df)

    # Fake detection
    df = detect_fake_reviews(df)

    # Train predictor on this dataset
    predictor.fit(df["review_text"].tolist(), df["rating"].tolist())

    # Build response
    total = len(df)
    fake_count = (df["fake_score"] >= 0.3).sum()

    overview = {
        "total_reviews": int(total),
        "avg_rating": round(float(df["rating"].mean()), 2),
        "sentiment_score": round(float(df["sentiment_score"].mean()), 3),
        "fake_review_percentage": round(float(fake_count) / total * 100, 1) if total else 0.0,
    }

    rating_dist = df["rating"].value_counts().sort_index().to_dict()
    rating_distribution = {str(k): int(v) for k, v in rating_dist.items()}

    topics = extract_topics_by_sentiment(df)
    word_frequencies = get_word_frequencies_by_sentiment(df)

    # Key insights: top complaint and praise phrases
    positive_df = df[df["sentiment"] == "positive"]
    negative_df = df[df["sentiment"] == "negative"]

    from .analysis.insights import extract_key_insights
    key_insights = extract_key_insights(positive_df, negative_df)

    suspicious = get_suspicious_reviews(df)

    sample_reviews = []
    for _, row in df.sample(min(20, len(df)), random_state=42).iterrows():
        sample_reviews.append({
            "text": row["review_text"][:500],
            "rating": int(row["rating"]),
            "sentiment": row["sentiment"],
            "sentiment_score": round(float(row["sentiment_score"]), 3),
        })

    sentiment_breakdown = get_sentiment_breakdown(df)
    timeline = build_sentiment_timeline(df)

    # Product detection and AI overview
    product_info = detect_products(df)
    ai_overview = generate_overview_summary(df, product_info, key_insights)

    result = {
        "overview": overview,
        "sentiment_timeline": timeline,
        "rating_distribution": rating_distribution,
        "topics": topics,
        "word_frequencies": word_frequencies,
        "key_insights": key_insights,
        "suspicious_reviews": suspicious,
        "sample_reviews": sample_reviews,
        "sentiment_breakdown": sentiment_breakdown,
        "product_info": product_info,
        "ai_overview": ai_overview,
    }
    # Use NumpyEncoder to handle numpy int64/float64 types
    content = json.loads(json.dumps(result, cls=NumpyEncoder))
    return JSONResponse(content=content)


# Prediction endpoint that uses the trained predictor to predict rating from review text
@app.post("/api/predict", response_model=PredictResponse)
async def predict_rating(req: PredictRequest):
    result = predictor.predict(req.text)
    return PredictResponse(**result)


# Endpoint to list available sample datasets
@app.get("/api/sample-data", response_model=list[SampleDatasetInfo])
def list_sample_data():
    datasets = []
    if os.path.isdir(SAMPLE_DATA_DIR):
        for fname in os.listdir(SAMPLE_DATA_DIR):
            if fname.endswith(".csv"):
                path = os.path.join(SAMPLE_DATA_DIR, fname)
                try:
                    row_count = sum(1 for _ in open(path, encoding="utf-8")) - 1
                except Exception:
                    row_count = 0
                datasets.append(SampleDatasetInfo(
                    id=fname,
                    name=fname.replace("_", " ").replace(".csv", "").title(),
                    description=f"Sample dataset with {row_count} reviews",
                    review_count=row_count,
                ))
    return datasets


# Endpoint to load a sample dataset by ID and return its file_id for analysis
@app.post("/api/load-sample/{dataset_id}")
async def load_sample(dataset_id: str):
    path = os.path.join(SAMPLE_DATA_DIR, dataset_id)
    if not os.path.isfile(path):
        raise HTTPException(404, "Sample dataset not found")

    df = pd.read_csv(path)
    df = preprocess_dataframe(df)
    file_id = str(uuid.uuid4())
    _uploads[file_id] = df

    return {
        "file_id": file_id,
        "filename": dataset_id,
        "total_rows": len(df),
        "message": "Sample data loaded successfully",
    }
