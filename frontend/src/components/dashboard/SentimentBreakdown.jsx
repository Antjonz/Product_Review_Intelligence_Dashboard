import { useState } from 'react'
import { sentimentColor, ratingStars } from '../../utils/formatters'

export default function SentimentBreakdown({ reviews, breakdown }) {
  const [page, setPage] = useState(0)
  const perPage = 5

  if (!reviews || reviews.length === 0) return null

  const totalPages = Math.ceil(reviews.length / perPage)
  const pageReviews = reviews.slice(page * perPage, (page + 1) * perPage)

  const total = (breakdown?.positive || 0) + (breakdown?.negative || 0) + (breakdown?.neutral || 0)

  return (
    <div>
      {/* Breakdown bar */}
      {breakdown && total > 0 && (
        <div className="mb-6">
          <div className="flex rounded-full overflow-hidden h-4 mb-2">
            <div style={{ width: `${(breakdown.positive / total) * 100}%` }} className="bg-green-500" />
            <div style={{ width: `${(breakdown.neutral / total) * 100}%` }} className="bg-gray-400" />
            <div style={{ width: `${(breakdown.negative / total) * 100}%` }} className="bg-red-500" />
          </div>
          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span className="text-green-600 dark:text-green-400">Positive: {breakdown.positive}</span>
            <span>Neutral: {breakdown.neutral}</span>
            <span className="text-red-600 dark:text-red-400">Negative: {breakdown.negative}</span>
          </div>
        </div>
      )}

      {/* Reviews */}
      <div className="space-y-3">
        {pageReviews.map((r, i) => (
          <div key={i} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <span
                className="w-3 h-3 rounded-full shrink-0"
                style={{ backgroundColor: sentimentColor(r.sentiment) }}
              />
              <span className="text-sm font-medium capitalize" style={{ color: sentimentColor(r.sentiment) }}>
                {r.sentiment}
              </span>
              <span className="text-yellow-500 text-sm">{ratingStars(r.rating)}</span>
              <span className="text-xs text-gray-400 ml-auto">Score: {r.sentiment_score}</span>
            </div>
            <p className="text-sm text-gray-700 dark:text-gray-300">{r.text}</p>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-4">
          <button
            onClick={() => setPage(Math.max(0, page - 1))}
            disabled={page === 0}
            className="px-3 py-1 text-sm rounded-lg bg-gray-200 dark:bg-gray-700 disabled:opacity-40 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            Prev
          </button>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {page + 1} / {totalPages}
          </span>
          <button
            onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
            disabled={page >= totalPages - 1}
            className="px-3 py-1 text-sm rounded-lg bg-gray-200 dark:bg-gray-700 disabled:opacity-40 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}
