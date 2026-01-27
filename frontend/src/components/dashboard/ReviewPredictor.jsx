import { useState, useEffect, useRef } from 'react'
import { predictRating } from '../../services/api'
import { ratingStars, sentimentColor } from '../../utils/formatters'
import { Brain } from 'lucide-react'

export default function ReviewPredictor() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const debounceRef = useRef(null)

  useEffect(() => {
    if (text.length < 10) {
      setResult(null)
      return
    }

    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(async () => {
      setLoading(true)
      try {
        const res = await predictRating(text)
        setResult(res)
      } catch {
        setResult(null)
      } finally {
        setLoading(false)
      }
    }, 500)

    return () => clearTimeout(debounceRef.current)
  }, [text])

  return (
    <div>
      <div className="flex items-center gap-2 mb-4">
        <Brain className="w-5 h-5 text-blue-500" />
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Type a review and the ML model will predict its rating and sentiment in real-time.
        </p>
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a product review here... (e.g., 'This product is amazing, works perfectly and great value for the price!')"
        className="w-full h-32 p-4 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
      />

      {loading && (
        <div className="mt-4 text-center text-gray-400 text-sm">Predicting...</div>
      )}

      {result && !loading && (
        <div className="mt-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl p-6 animate-fade-in">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Predicted Rating</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{result.predicted_rating}</p>
              <p className="text-yellow-500 mt-1">{ratingStars(result.predicted_rating)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Sentiment</p>
              <p className="text-2xl font-bold capitalize" style={{ color: sentimentColor(result.sentiment) }}>
                {result.sentiment}
              </p>
              <p className="text-sm text-gray-400 mt-1">Score: {result.sentiment_score}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Confidence</p>
              <p className="text-3xl font-bold text-blue-500">{(result.confidence * 100).toFixed(0)}%</p>
              <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mt-2">
                <div className="bg-blue-500 h-2 rounded-full transition-all" style={{ width: `${result.confidence * 100}%` }} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
