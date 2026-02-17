/// TopicBubbles.jsx
// This component displays the main topics extracted from the reviews, categorized into positive and negative topics. 
// It uses a treemap visualization to show the relative size of each topic based on how many reviews mentioned it. 
// Each bubble is colored differently and shows the topic name, and hovering over it reveals the top keywords associated with that topic.

import { Treemap, ResponsiveContainer, Tooltip } from 'recharts'

const POSITIVE_COLORS = ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0']
const NEGATIVE_COLORS = ['#ef4444', '#f87171', '#fca5a5', '#fecaca']

function CustomContent({ x, y, width, height, name, fill }) {
  if (width < 40 || height < 30) return null
  return (
    <g>
      <rect x={x} y={y} width={width} height={height} fill={fill} rx={4} stroke="#fff" strokeWidth={2} />
      <text x={x + width / 2} y={y + height / 2} textAnchor="middle" dominantBaseline="central" fill="#fff" fontSize={Math.min(14, width / 6)} fontWeight="600">
        {name}
      </text>
    </g>
  )
}

function TopicTree({ title, topics, colors }) {
  if (!topics || topics.length === 0) {
    return (
      <div>
        <h4 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">{title}</h4>
        <p className="text-xs text-gray-400">No topics found</p>
      </div>
    )
  }

  const data = topics.map((t, i) => ({
    name: t.name,
    size: t.count,
    fill: colors[i % colors.length],
    keywords: t.keywords,
  }))

  return (
    <div>
      <h4 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">{title}</h4>
      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <Treemap
            data={data}
            dataKey="size"
            nameKey="name"
            content={<CustomContent />}
          >
            <Tooltip
              content={({ payload }) => {
                if (!payload?.[0]) return null
                const d = payload[0].payload
                return (
                  <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3 shadow-lg">
                    <p className="font-semibold">{d.name}</p>
                    <p className="text-xs text-gray-500 mt-1">{d.keywords?.slice(0, 5).join(', ')}</p>
                  </div>
                )
              }}
            />
          </Treemap>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default function TopicBubbles({ topics }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Topic Clusters</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TopicTree title="Positive Topics" topics={topics?.positive} colors={POSITIVE_COLORS} />
        <TopicTree title="Negative Topics" topics={topics?.negative} colors={NEGATIVE_COLORS} />
      </div>
    </div>
  )
}
