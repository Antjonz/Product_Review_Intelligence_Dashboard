# Product Review Intelligence Dashboard

A fullstack web application that analyzes product review datasets using machine learning, providing sentiment analysis, topic extraction, fake review detection, and predictive analytics through an interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)

## Features

- **Sentiment Analysis** — VADER-based sentiment scoring with positive/negative/neutral classification and timeline trends
- **Topic Extraction** — LDA topic modeling to discover key themes in positive and negative reviews
- **Fake Review Detection** — Heuristic anomaly detection identifying suspicious reviews based on length, sentiment-rating mismatch, repetition, and extreme polarity
- **Rating Prediction** — Ridge regression model predicts star ratings from review text with confidence scores
- **Interactive Dashboard** — Real-time visualizations including charts, word clouds, and filterable tables
- **Dark Mode** — Full light/dark theme support

## Tech Stack

### Backend
- FastAPI (Python 3.11+)
- Pandas / NumPy for data processing
- VADER for sentiment analysis
- scikit-learn for topic modeling (LDA) and rating prediction (Ridge)

### Frontend
- React 18 with Vite
- TailwindCSS for styling
- Recharts for data visualizations
- React Query for server state
- react-dropzone for file uploads
- Lucide React for icons

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python generate_sample_data.py
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a CSV file for analysis |
| `POST` | `/api/analyze?file_id=<id>` | Run full analysis pipeline |
| `POST` | `/api/predict` | Predict rating from review text |
| `GET` | `/api/sample-data` | List available sample datasets |
| `POST` | `/api/load-sample/<id>` | Load a sample dataset |

### Analysis Response

The `/api/analyze` endpoint returns:

```json
{
  "overview": { "total_reviews": 1000, "avg_rating": 3.5, "sentiment_score": 0.2, "fake_review_percentage": 5.0 },
  "sentiment_timeline": [{ "period": "2024-01", "positive": 60, "negative": 25, "neutral": 15, "avg_sentiment": 0.3 }],
  "rating_distribution": { "1": 100, "2": 150, "3": 200, "4": 250, "5": 300 },
  "topics": { "positive": [], "negative": [] },
  "word_frequencies": { "positive": [], "negative": [] },
  "key_insights": { "complaints": [], "praises": [] },
  "suspicious_reviews": [],
  "sample_reviews": [],
  "sentiment_breakdown": { "positive": 500, "negative": 300, "neutral": 200 }
}
```

### CSV Format

Upload files must contain at minimum:
- `review_text` (or `text`, `comment`, `feedback`) — the review content
- `rating` (or `score`, `stars`, `overall`) — numeric rating 1-5
- `date` (optional) — enables timeline analysis

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app and endpoints
│   │   ├── models.py            # Pydantic response models
│   │   ├── analysis/
│   │   │   ├── sentiment.py     # VADER sentiment analysis
│   │   │   ├── topics.py        # LDA topic extraction
│   │   │   ├── fake_detection.py # Suspicious review detection
│   │   │   └── predictions.py   # Rating prediction model
│   │   └── utils/
│   │       └── data_processing.py # CSV preprocessing
│   ├── sample_data/
│   │   └── amazon_reviews.csv
│   ├── generate_sample_data.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── layout/          # Header, Layout
│   │   │   ├── upload/          # FileUpload with drag-and-drop
│   │   │   ├── dashboard/       # All visualization components
│   │   │   └── common/          # LoadingSpinner, ErrorMessage
│   │   ├── hooks/useAnalysis.js
│   │   ├── services/api.js
│   │   └── utils/formatters.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## Future Improvements

- Transformer-based sentiment (DistilBERT) for higher accuracy
- Database persistence (PostgreSQL/SQLite) for uploaded datasets
- User authentication and saved analysis history
- Export analysis reports as PDF
- Comparison mode for multiple products
- Real-time streaming analysis for large datasets
- Docker Compose for one-command deployment
