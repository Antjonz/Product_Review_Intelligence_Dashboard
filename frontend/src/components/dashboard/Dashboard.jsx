import { useState } from 'react'
import OverviewCards from './OverviewCards'
import SentimentTimeline from './SentimentTimeline'
import RatingDistribution from './RatingDistribution'
import TopicBubbles from './TopicBubbles'
import WordClouds from './WordClouds'
import KeyInsights from './KeyInsights'
import SuspiciousReviews from './SuspiciousReviews'
import SentimentBreakdown from './SentimentBreakdown'
import ReviewPredictor from './ReviewPredictor'

const TABS = [
  { id: 'insights', label: 'Key Insights' },
  { id: 'suspicious', label: 'Suspicious Reviews' },
  { id: 'sentiment', label: 'Sentiment Analysis' },
  { id: 'predict', label: 'Predict Rating' },
]

export default function Dashboard({ data }) {
  const [activeTab, setActiveTab] = useState('insights')

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Overview */}
      <OverviewCards overview={data.overview} />

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SentimentTimeline data={data.sentiment_timeline} />
        <RatingDistribution data={data.rating_distribution} />
      </div>

      {/* Topics and Word Clouds */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopicBubbles topics={data.topics} />
        <WordClouds frequencies={data.word_frequencies} />
      </div>

      {/* Tabbed deep dive */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 animate-fade-in">
        <div className="border-b border-gray-200 dark:border-gray-700">
          <nav className="flex overflow-x-auto">
            {TABS.map(({ id, label }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`px-6 py-3 text-sm font-medium whitespace-nowrap transition-colors border-b-2 ${
                  activeTab === id
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
        <div className="p-6">
          {activeTab === 'insights' && <KeyInsights insights={data.key_insights} />}
          {activeTab === 'suspicious' && <SuspiciousReviews reviews={data.suspicious_reviews} />}
          {activeTab === 'sentiment' && (
            <SentimentBreakdown reviews={data.sample_reviews} breakdown={data.sentiment_breakdown} />
          )}
          {activeTab === 'predict' && <ReviewPredictor />}
        </div>
      </div>
    </div>
  )
}
