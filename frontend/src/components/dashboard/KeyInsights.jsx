/// KeyInsights.jsx
// This component displays the key insights extracted from the reviews, categorized into what customers love and common complaints. 
// Each insight is shown with a thumbs up or down icon and a count of how many reviews mentioned it. If there are no insights, it shows a placeholder message.

import { ThumbsUp, ThumbsDown } from 'lucide-react'

function InsightList({ items, icon: Icon, colorClass, badgeClass }) {
  if (!items || items.length === 0) return <p className="text-sm text-gray-400">No insights found</p>
  return (
    <ul className="space-y-2">
      {items.map((item, i) => (
        <li key={i} className="flex items-center justify-between">
          <span className="flex items-center gap-2">
            <Icon className={`w-4 h-4 ${colorClass}`} />
            <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">{item.text}</span>
          </span>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${badgeClass}`}>
            {item.count}
          </span>
        </li>
      ))}
    </ul>
  )
}

export default function KeyInsights({ insights }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">What Customers Love</h3>
        <InsightList
          items={insights?.praises}
          icon={ThumbsUp}
          colorClass="text-green-500"
          badgeClass="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400"
        />
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Common Complaints</h3>
        <InsightList
          items={insights?.complaints}
          icon={ThumbsDown}
          colorClass="text-red-500"
          badgeClass="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400"
        />
      </div>
    </div>
  )
}
