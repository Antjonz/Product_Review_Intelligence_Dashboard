export default function LoadingSpinner({ message = 'Analyzing reviews...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 animate-fade-in">
      <div className="w-12 h-12 border-4 border-blue-200 dark:border-blue-800 border-t-blue-500 rounded-full animate-spin mb-4" />
      <p className="text-gray-600 dark:text-gray-300 text-lg">{message}</p>
      <p className="text-gray-400 dark:text-gray-500 text-sm mt-1">This may take a moment for large datasets</p>
    </div>
  )
}
