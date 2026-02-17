/// SuspiciousReviews.jsx
// This component displays a list of reviews that have been flagged as suspicious by the ML model. Each review shows the text (truncated if not expanded), the reasons why it was flagged, the predicted rating, and the fake score. 
// Users can click on a review to expand and see the full text. If there are no suspicious reviews, it shows a placeholder message with an icon.

import { useState } from 'react'
import { ShieldAlert } from 'lucide-react'
import { ratingStars, truncate } from '../../utils/formatters'

export default function SuspiciousReviews({ reviews }) {
  const [sortBy, setSortBy] = useState('fake_score')
  const [expanded, setExpanded] = useState(null)

  if (!reviews || reviews.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400">
        <ShieldAlert className="w-10 h-10 mx-auto mb-2 opacity-50" />
        <p>No suspicious reviews detected</p>
      </div>
    )
  }

  const sorted = [...reviews].sort((a, b) => b[sortBy] - a[sortBy])

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-gray-500 dark:text-gray-400">{reviews.length} suspicious reviews found</p>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="text-sm border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300"
        >
          <option value="fake_score">Sort by Fake Score</option>
          <option value="rating">Sort by Rating</option>
        </select>
      </div>
      <div className="space-y-3">
        {sorted.map((r, i) => (
          <div
            key={i}
            className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            onClick={() => setExpanded(expanded === i ? null : i)}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {expanded === i ? r.text : truncate(r.text, 120)}
                </p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {r.reasons.map((reason, j) => (
                    <span key={j} className="text-xs bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 px-2 py-0.5 rounded-full">
                      {reason}
                    </span>
                  ))}
                </div>
              </div>
              <div className="text-right shrink-0">
                <p className="text-sm text-yellow-500">{ratingStars(r.rating)}</p>
                <p className={`text-lg font-bold ${r.fake_score > 0.6 ? 'text-red-500' : 'text-orange-500'}`}>
                  {(r.fake_score * 100).toFixed(0)}%
                </p>
                <p className="text-xs text-gray-400">fake score</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
