from pydantic import BaseModel, Field
from typing import Optional


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    total_rows: int
    columns: list[str]
    message: str


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=5000)


class PredictResponse(BaseModel):
    predicted_rating: float
    confidence: float
    sentiment: str
    sentiment_score: float


class OverviewStats(BaseModel):
    total_reviews: int
    avg_rating: float
    sentiment_score: float
    fake_review_percentage: float


class TopicInfo(BaseModel):
    name: str
    keywords: list[str]
    count: int
    weight: float


class SuspiciousReview(BaseModel):
    index: int
    text: str
    rating: int
    fake_score: float
    reasons: list[str]


class InsightItem(BaseModel):
    text: str
    count: int
    sentiment: str


class SentimentTimelinePoint(BaseModel):
    period: str
    positive: float
    negative: float
    neutral: float
    avg_sentiment: float


class ReviewSample(BaseModel):
    text: str
    rating: int
    sentiment: str
    sentiment_score: float


class AnalysisResponse(BaseModel):
    overview: OverviewStats
    sentiment_timeline: list[SentimentTimelinePoint]
    rating_distribution: dict[str, int]
    topics: dict[str, list[TopicInfo]]
    word_frequencies: dict[str, list[dict]]
    key_insights: dict[str, list[InsightItem]]
    suspicious_reviews: list[SuspiciousReview]
    sample_reviews: list[ReviewSample]
    sentiment_breakdown: dict[str, int]


class SampleDatasetInfo(BaseModel):
    id: str
    name: str
    description: str
    review_count: int
