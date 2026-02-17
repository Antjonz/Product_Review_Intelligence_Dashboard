/// WordClouds.jsx
// This component displays word clouds for the most frequently mentioned words in positive and negative reviews. 
// It sizes the words based on their frequency and colors them differently for positive and negative sentiments. 
// If there are no words to display, it shows a placeholder message.


function WordCloud({ words, colorClass }) {
  if (!words || words.length === 0) return <p className="text-xs text-gray-400">No data</p>

  const maxCount = Math.max(...words.map((w) => w.count))

  return (
    <div className="flex flex-wrap gap-2 justify-center">
      {words.slice(0, 30).map(({ word, count }) => {
        const ratio = count / maxCount
        const size = 12 + ratio * 20
        const opacity = 0.4 + ratio * 0.6
        return (
          <span
            key={word}
            className={`${colorClass} font-medium cursor-default transition-transform hover:scale-110`}
            style={{ fontSize: `${size}px`, opacity }}
            title={`${word}: ${count} mentions`}
          >
            {word}
          </span>
        )
      })}
    </div>
  )
}

export default function WordClouds({ frequencies }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 animate-fade-in">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Word Frequencies</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 className="text-sm font-medium text-green-600 dark:text-green-400 mb-3 text-center">Positive Reviews</h4>
          <WordCloud words={frequencies?.positive} colorClass="text-green-600 dark:text-green-400" />
        </div>
        <div>
          <h4 className="text-sm font-medium text-red-600 dark:text-red-400 mb-3 text-center">Negative Reviews</h4>
          <WordCloud words={frequencies?.negative} colorClass="text-red-600 dark:text-red-400" />
        </div>
      </div>
    </div>
  )
}
