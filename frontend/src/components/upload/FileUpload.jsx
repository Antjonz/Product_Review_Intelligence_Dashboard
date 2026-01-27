import { useCallback, useState, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Database, Sparkles, BarChart3, Shield, Brain } from 'lucide-react'
import { getSampleDatasets } from '../../services/api'

export default function FileUpload({ onUpload, onLoadSample, loading }) {
  const [samples, setSamples] = useState([])

  useEffect(() => {
    getSampleDatasets().then(setSamples).catch(() => {})
  }, [])

  const onDrop = useCallback((accepted) => {
    if (accepted.length > 0) onUpload(accepted[0])
  }, [onUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    maxFiles: 1,
    disabled: loading,
  })

  const features = [
    { icon: Sparkles, title: 'Sentiment Analysis', desc: 'AI-powered sentiment scoring for every review' },
    { icon: BarChart3, title: 'Topic Extraction', desc: 'Discover key themes using LDA topic modeling' },
    { icon: Shield, title: 'Fake Detection', desc: 'Identify suspicious reviews with anomaly detection' },
    { icon: Brain, title: 'Rating Prediction', desc: 'Predict ratings from review text with ML' },
  ]

  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <div className="text-center mb-10">
        <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
          Product Review Intelligence
        </h2>
        <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
          Upload a CSV of product reviews and get instant AI-powered insights including
          sentiment analysis, topic extraction, and fake review detection.
        </p>
      </div>

      {/* Upload zone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all
          ${isDragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 hover:bg-gray-50 dark:hover:bg-gray-800'}
          ${loading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
        {isDragActive ? (
          <p className="text-blue-500 text-lg font-medium">Drop your CSV file here</p>
        ) : (
          <>
            <p className="text-gray-700 dark:text-gray-300 text-lg font-medium">
              Drag & drop a CSV file, or click to browse
            </p>
            <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">
              Must contain <code className="bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded text-xs">review_text</code> and{' '}
              <code className="bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded text-xs">rating</code> columns
            </p>
          </>
        )}
      </div>

      {/* Sample data */}
      {samples.length > 0 && (
        <div className="mt-6 text-center">
          <p className="text-gray-500 dark:text-gray-400 text-sm mb-3">Or try a sample dataset:</p>
          <div className="flex flex-wrap justify-center gap-3">
            {samples.map((s) => (
              <button
                key={s.id}
                onClick={() => onLoadSample(s.id)}
                disabled={loading}
                className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all text-sm disabled:opacity-50"
              >
                <Database className="w-4 h-4 text-blue-500" />
                <span className="text-gray-700 dark:text-gray-300">{s.name}</span>
                <span className="text-gray-400 text-xs">({s.review_count} reviews)</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Feature highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-12">
        {features.map(({ icon: Icon, title, desc }) => (
          <div key={title} className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700">
            <Icon className="w-8 h-8 text-blue-500 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{title}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
