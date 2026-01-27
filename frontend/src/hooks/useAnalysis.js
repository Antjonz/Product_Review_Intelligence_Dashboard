import { useState, useCallback } from 'react'
import { uploadFile, analyzeData, loadSampleDataset } from '../services/api'

export function useAnalysis() {
  const [fileId, setFileId] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [uploadInfo, setUploadInfo] = useState(null)

  const handleUpload = useCallback(async (file) => {
    setLoading(true)
    setError(null)
    try {
      const info = await uploadFile(file)
      setUploadInfo(info)
      setFileId(info.file_id)
      const result = await analyzeData(info.file_id)
      setAnalysis(result)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }, [])

  const handleLoadSample = useCallback(async (datasetId) => {
    setLoading(true)
    setError(null)
    try {
      const info = await loadSampleDataset(datasetId)
      setUploadInfo(info)
      setFileId(info.file_id)
      const result = await analyzeData(info.file_id)
      setAnalysis(result)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load sample data')
    } finally {
      setLoading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setFileId(null)
    setAnalysis(null)
    setError(null)
    setUploadInfo(null)
  }, [])

  return { fileId, analysis, loading, error, uploadInfo, handleUpload, handleLoadSample, reset }
}
