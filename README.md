# Product Review Intelligence Dashboard

A fullstack web application that analyzes product review datasets using machine learning, providing sentiment analysis, topic extraction, fake review detection, and predictive analytics through an interactive dashboard.

This is a demo learning project using the skills I've learned from my Data science/Machine learning, and Full-stack development courses.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)

![Demo](Screenshots/Product%20Review%20Intelligence%20Dashboard.gif.gif)

## Features

| Feature | Description | Preview |
|---------|-------------|---------|
| **File Upload & Sample Data** | Drag-and-drop CSV upload or browse pre-generated sample datasets. Automatic validation and preprocessing with support for multiple column name formats. | <img src="Screenshots/01%20homepage.png" width="300"> |
| **AI Overview & Statistics** | Automatic product detection with category identification, key terms extraction, and natural language summary. Overview cards show total reviews, average rating, overall sentiment score, and fake review percentage. | <img src="Screenshots/02%20dashboard%20ai%20overview.png" width="300"><br><img src="Screenshots/02%20stats.png" width="300"> |
| **Key Insights** | Advanced TF-IDF analysis extracts distinctive praise and complaint phrases from reviews, mapped back to actual sentences for human-readable insights. Highlights what customers specifically love and hate. | <img src="Screenshots/03%20general%20insights.png" width="300"> |
| **Fake Review Detection** | Heuristic anomaly detection identifies suspicious reviews based on length anomalies, sentiment-rating mismatch, text repetition, and extreme polarity. Sortable and filterable table with fake scores and detection reasons. | <img src="Screenshots/04%20suspicious%20reviews.png" width="300"> |
| **Sentiment Analysis** | VADER-based sentiment scoring with positive/negative/neutral classification. Interactive visualizations include sentiment breakdown pie chart, timeline trends over time, rating distribution bar chart, topic bubbles for theme discovery, and word clouds for frequent terms. | <img src="Screenshots/05%20sentiment%20analysis.png" width="300"> |
| **Rating Predictor** | Interactive widget using Ridge regression to predict star ratings from custom review text. Enter any review and get instant rating prediction with confidence scores. Model trains automatically on your uploaded dataset. | <img src="Screenshots/06%20rating%20predictor.png" width="300"> |
| **Dark Mode** | Full light/dark theme support with persistent user preference stored in localStorage. Toggle between themes with smooth transitions. | |

## Tech Stack

### Backend
- **FastAPI** (Python 3.11+) — Modern async web framework with automatic API documentation
- **Pandas / NumPy** — Data manipulation and numerical computing
- **VADER Sentiment** — Lexicon-based sentiment analysis optimized for social media text
- **scikit-learn** — Machine learning toolkit for LDA topic modeling and Ridge regression
- **TF-IDF Vectorization** — Extract distinctive phrases and insights from review text

### Frontend
- **React 18** with Vite — Fast, modern development with HMR
- **TailwindCSS** — Utility-first CSS framework for responsive, dark-mode-ready UI
- **Recharts** — Composable charting library for data visualizations (line charts, pie charts, bar charts)
- **TanStack Query (React Query)** — Powerful async state management for API calls
- **react-dropzone** — Drag-and-drop file upload with validation
- **Lucide React** — Beautiful, consistent icon set
- **Axios** — HTTP client for backend communication

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python generate_sample_data.py # Generate sample dataset (optional)
uvicorn app.main:app --reload --port 8000
```

Backend will be running at `http://localhost:8000`  
API documentation available at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be running at `http://localhost:5173`

### Quick Start (Windows)

Run `start.bat` to launch both servers simultaneously.

## Usage

1. **Upload Data**: Drag and drop a CSV file or browse sample datasets
2. **Automatic Analysis**: Analysis runs automatically after upload
3. **Explore Dashboard**: Interactive visualizations update in real-time
4. **Test Predictions**: Use the rating predictor to test custom review text
5. **Filter Suspicious Reviews**: Sort and filter the fake review detection table

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check endpoint |
| `POST` | `/api/upload` | Upload a CSV file for analysis |
| `POST` | `/api/analyze?file_id=<id>` | Run full analysis pipeline on uploaded file |
| `POST` | `/api/predict` | Predict rating from review text using trained model |
| `GET` | `/api/sample-data` | List available sample datasets with metadata |
| `POST` | `/api/load-sample/<id>` | Load a sample dataset by filename |



### CSV Format

Upload files must contain at minimum:
- `review_text` (or `text`, `comment`, `feedback`, `reviewText`) — the review content
- `rating` (or `score`, `stars`, `overall`) — numeric rating 1-5

Optional columns for enhanced features:
- `date` (or `timestamp`, `review_date`) — enables sentiment timeline analysis
- `product_id` (or `asin`, `product_name`) — enables product-specific grouping and detection

The system automatically detects and normalizes common column name variations.


## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app and API endpoints
│   │   ├── models.py               # Pydantic request/response models
│   │   ├── analysis/
│   │   │   ├── sentiment.py        # VADER sentiment analysis & timeline
│   │   │   ├── topics.py           # LDA topic extraction & word frequencies
│   │   │   ├── fake_detection.py   # Heuristic fake review detection
│   │   │   ├── predictions.py      # Ridge regression rating predictor
│   │   │   ├── product_overview.py # Product detection & AI overview
│   │   │   └── insights.py         # TF-IDF key insights extraction
│   │   └── utils/
│   │       └── data_processing.py  # CSV preprocessing & validation
│   ├── sample_data/
│   │   └── amazon_reviews.csv      # Sample dataset for testing
│   ├── generate_sample_data.py     # Script to create sample datasets
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main app component with dark mode
│   │   ├── main.jsx                # React entry point
│   │   ├── index.css               # Tailwind CSS imports
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.jsx      # App header with dark mode toggle
│   │   │   │   └── Layout.jsx      # Main layout wrapper
│   │   │   ├── upload/
│   │   │   │   └── FileUpload.jsx  # Drag-and-drop + sample data browser
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.jsx           # Main dashboard orchestrator
│   │   │   │   ├── OverviewCards.jsx       # Summary statistics cards
│   │   │   │   ├── AIOverview.jsx          # Product info & AI summary
│   │   │   │   ├── KeyInsights.jsx         # Praise/complaint insights
│   │   │   │   ├── SentimentBreakdown.jsx  # Pie chart visualization
│   │   │   │   ├── SentimentTimeline.jsx   # Line chart over time
│   │   │   │   ├── RatingDistribution.jsx  # Bar chart of ratings
│   │   │   │   ├── TopicBubbles.jsx        # Bubble chart for topics
│   │   │   │   ├── WordClouds.jsx          # Word frequency clouds
│   │   │   │   ├── SuspiciousReviews.jsx   # Fake review table
│   │   │   │   └── ReviewPredictor.jsx     # Interactive rating predictor
│   │   │   └── common/
│   │   │       ├── LoadingSpinner.jsx      # Loading state UI
│   │   │       └── ErrorMessage.jsx        # Error state UI
│   │   ├── hooks/
│   │   │   └── useAnalysis.js      # Custom hook for analysis workflow
│   │   ├── services/
│   │   │   └── api.js              # Axios API client
│   │   └── utils/
│   │       └── formatters.js       # Number & text formatting utilities
│   ├── package.json                # npm dependencies & scripts
│   ├── vite.config.js              # Vite build configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   └── postcss.config.js           # PostCSS configuration
│
├── start.bat                       # Windows batch script to start both servers
└── README.md                       # This file
```

## Key Components

### Backend Analysis Pipeline

1. **Data Preprocessing** (`data_processing.py`)
   - CSV parsing with flexible column name detection
   - Data validation and normalization
   - Tokenization and text cleaning

2. **Sentiment Analysis** (`sentiment.py`)
   - VADER-based compound sentiment scoring
   - Three-class classification (positive/negative/neutral)
   - Timeline aggregation by time period
   - Sentiment breakdown statistics

3. **Topic Modeling** (`topics.py`)
   - LDA (Latent Dirichlet Allocation) for theme discovery
   - Separate topic extraction for positive and negative reviews
   - Word frequency analysis for word cloud generation
   - Configurable number of topics and top keywords

4. **Fake Review Detection** (`fake_detection.py`)
   - Multi-factor heuristic scoring:
     - Review length anomalies
     - Sentiment-rating mismatch detection
     - Extreme polarity identification
     - Text repetition analysis
   - Adjustable threshold for suspicious classification

5. **Rating Prediction** (`predictions.py`)
   - TF-IDF vectorization of review text
   - Ridge regression model training
   - Confidence scoring based on prediction uncertainty
   - Real-time prediction API

6. **Product Detection** (`product_overview.py`)
   - Product ID extraction from structured data
   - Category matching against known product types
   - Key term and phrase frequency analysis
   - Bigram extraction for compound product names

7. **Key Insights** (`insights.py`)
   - Advanced TF-IDF analysis on bigrams and trigrams
   - Distinctive phrase extraction (praise vs complaints)
   - Sentence mapping to find readable context
   - Automatic filtering of generic phrases

### Frontend Architecture

- **State Management**: TanStack Query for server state, React hooks for UI state
- **Responsive Design**: Mobile-first Tailwind CSS with dark mode support
- **Component Structure**: Modular, reusable components with clear separation of concerns
- **Data Visualization**: Recharts for interactive charts with hover states and animations
- **Error Handling**: Comprehensive error boundaries and user-friendly error messages
- **Performance**: Lazy loading, memoization, and optimized re-renders


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
