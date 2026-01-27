import { useState, useEffect } from 'react'
import Layout from './components/layout/Layout'
import FileUpload from './components/upload/FileUpload'
import Dashboard from './components/dashboard/Dashboard'
import LoadingSpinner from './components/common/LoadingSpinner'
import ErrorMessage from './components/common/ErrorMessage'
import { useAnalysis } from './hooks/useAnalysis'

export default function App() {
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('darkMode') === 'true' ||
        window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return false
  })

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode)
    document.documentElement.classList.toggle('dark', darkMode)
  }, [darkMode])

  const { analysis, loading, error, handleUpload, handleLoadSample, reset } = useAnalysis()

  return (
    <Layout darkMode={darkMode} setDarkMode={setDarkMode} showBack={!!analysis} onBack={reset}>
      {loading && <LoadingSpinner />}
      {error && !loading && <ErrorMessage message={error} onRetry={reset} />}
      {!loading && !error && !analysis && (
        <FileUpload onUpload={handleUpload} onLoadSample={handleLoadSample} loading={loading} />
      )}
      {!loading && !error && analysis && <Dashboard data={analysis} />}
    </Layout>
  )
}
