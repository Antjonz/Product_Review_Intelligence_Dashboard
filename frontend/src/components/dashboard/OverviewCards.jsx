import { MessageSquare, Star, TrendingUp, ShieldAlert } from 'lucide-react'
import { formatNumber } from '../../utils/formatters'

const cards = [
  { key: 'total_reviews', label: 'Total Reviews', icon: MessageSquare, color: 'blue', format: formatNumber },
  { key: 'avg_rating', label: 'Avg Rating', icon: Star, color: 'yellow', format: (v) => v.toFixed(2) + ' / 5' },
  { key: 'sentiment_score', label: 'Sentiment Score', icon: TrendingUp, color: 'green', format: (v) => (v > 0 ? '+' : '') + v.toFixed(3) },
  { key: 'fake_review_percentage', label: 'Suspicious Reviews', icon: ShieldAlert, color: 'red', format: (v) => v.toFixed(1) + '%' },
]

const colorClasses = {
  blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
  yellow: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400',
  green: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
  red: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
}

export default function OverviewCards({ overview }) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map(({ key, label, icon: Icon, color, format }) => (
        <div key={key} className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm text-gray-500 dark:text-gray-400">{label}</span>
            <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
              <Icon className="w-4 h-4" />
            </div>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {format(overview[key])}
          </p>
        </div>
      ))}
    </div>
  )
}
