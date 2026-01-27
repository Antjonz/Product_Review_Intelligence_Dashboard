import { AlertCircle } from 'lucide-react'

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center animate-fade-in">
      <AlertCircle className="w-10 h-10 text-red-500 mx-auto mb-3" />
      <h3 className="text-red-700 dark:text-red-400 font-semibold text-lg">Something went wrong</h3>
      <p className="text-red-600 dark:text-red-300 mt-1">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 px-4 py-2 bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-200 rounded-lg hover:bg-red-200 dark:hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  )
}
