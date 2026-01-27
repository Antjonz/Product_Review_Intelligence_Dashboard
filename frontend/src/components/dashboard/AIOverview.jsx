import { Sparkles, Package, ThumbsUp, ThumbsDown, MessageSquare, Tag } from 'lucide-react'

export default function AIOverview({ aiOverview, productInfo }) {
  if (!aiOverview) return null

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-800 rounded-xl border border-blue-200 dark:border-gray-700 p-6 animate-fade-in">
      <div className="flex items-center gap-2 mb-5">
        <Sparkles className="w-5 h-5 text-blue-500" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Overview</h3>
      </div>

      {/* Product Detection */}
      {aiOverview.product_description && (
        <div className="flex items-start gap-3 mb-4">
          <Package className="w-4 h-4 text-indigo-500 mt-1 shrink-0" />
          <p className="text-sm text-gray-700 dark:text-gray-300">{aiOverview.product_description}</p>
        </div>
      )}

      {/* Detected Categories */}
      {productInfo?.detected_categories?.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4 ml-7">
          {productInfo.detected_categories.map((cat) => (
            <span
              key={cat.category}
              className="inline-flex items-center gap-1 px-2.5 py-1 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-full text-xs font-medium"
            >
              <Tag className="w-3 h-3" />
              {cat.category}
              <span className="text-indigo-400 dark:text-indigo-500">({cat.mentions})</span>
            </span>
          ))}
        </div>
      )}

      {/* Overall Summary */}
      <div className="flex items-start gap-3 mb-4">
        <MessageSquare className="w-4 h-4 text-blue-500 mt-1 shrink-0" />
        <p className="text-sm text-gray-700 dark:text-gray-300">{aiOverview.overall_summary}</p>
      </div>

      {/* What people like and dislike - side by side */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        {aiOverview.what_people_like && (
          <div className="bg-green-50 dark:bg-green-900/10 rounded-lg p-4 border border-green-200 dark:border-green-900/30">
            <div className="flex items-center gap-2 mb-2">
              <ThumbsUp className="w-4 h-4 text-green-600 dark:text-green-400" />
              <h4 className="text-sm font-semibold text-green-800 dark:text-green-300">What People Like</h4>
            </div>
            <p className="text-sm text-green-700 dark:text-green-300/80">{aiOverview.what_people_like}</p>
          </div>
        )}

        {aiOverview.what_people_dislike && (
          <div className="bg-red-50 dark:bg-red-900/10 rounded-lg p-4 border border-red-200 dark:border-red-900/30">
            <div className="flex items-center gap-2 mb-2">
              <ThumbsDown className="w-4 h-4 text-red-600 dark:text-red-400" />
              <h4 className="text-sm font-semibold text-red-800 dark:text-red-300">What People Dislike</h4>
            </div>
            <p className="text-sm text-red-700 dark:text-red-300/80">{aiOverview.what_people_dislike}</p>
          </div>
        )}
      </div>

      {/* Recommendation */}
      <div className="bg-white/60 dark:bg-gray-700/40 rounded-lg p-3 border border-gray-200 dark:border-gray-600">
        <p className="text-sm text-gray-700 dark:text-gray-300 font-medium">{aiOverview.recommendation}</p>
      </div>

      {/* Key terms */}
      {productInfo?.key_terms?.length > 0 && (
        <div className="mt-4">
          <p className="text-xs text-gray-400 dark:text-gray-500 mb-2">Frequently mentioned terms:</p>
          <div className="flex flex-wrap gap-1.5">
            {productInfo.key_terms.slice(0, 12).map((term) => (
              <span
                key={term}
                className="px-2 py-0.5 bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded text-xs border border-gray-200 dark:border-gray-600"
              >
                {term}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
