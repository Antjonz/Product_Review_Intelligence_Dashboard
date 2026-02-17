/// SentimentTimeline.jsx
// This component displays a line chart showing the percentage of positive, negative, and neutral reviews over time. 
// It uses the Recharts library to create a responsive line chart with a tooltip and legend for easy interpretation of the sentiment trends.

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

export default function SentimentTimeline({ data }) {
  if (!data || data.length === 0) return null

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Sentiment Over Time</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="period" tick={{ fontSize: 12 }} stroke="#9ca3af" />
            <YAxis tick={{ fontSize: 12 }} stroke="#9ca3af" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--tooltip-bg, #fff)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Line type="monotone" dataKey="positive" stroke="#10b981" strokeWidth={2} dot={false} name="Positive %" />
            <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={2} dot={false} name="Negative %" />
            <Line type="monotone" dataKey="neutral" stroke="#6b7280" strokeWidth={2} dot={false} name="Neutral %" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
