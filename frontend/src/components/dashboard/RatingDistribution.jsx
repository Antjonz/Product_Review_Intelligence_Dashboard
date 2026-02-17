/// RatingDistribution.jsx
// This component displays a bar chart of the rating distribution for the product. It shows how many reviews gave 1 star, 2 stars, etc. 
// The bars are colored differently for each rating level to make it visually appealing and easy to interpret at a glance.

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const COLORS = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#10b981']

export default function RatingDistribution({ data }) {
  if (!data) return null

  const chartData = [1, 2, 3, 4, 5].map((r) => ({
    rating: `${r} Star`,
    count: data[String(r)] || 0,
  }))

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Rating Distribution</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="rating" tick={{ fontSize: 12 }} stroke="#9ca3af" />
            <YAxis tick={{ fontSize: 12 }} stroke="#9ca3af" />
            <Tooltip />
            <Bar dataKey="count" radius={[6, 6, 0, 0]}>
              {chartData.map((_, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
