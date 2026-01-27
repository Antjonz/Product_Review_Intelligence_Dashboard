import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export async function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/upload', form)
  return data
}

export async function analyzeData(fileId) {
  const { data } = await api.post(`/analyze?file_id=${fileId}`)
  return data
}

export async function predictRating(text) {
  const { data } = await api.post('/predict', { text })
  return data
}

export async function getSampleDatasets() {
  const { data } = await api.get('/sample-data')
  return data
}

export async function loadSampleDataset(datasetId) {
  const { data } = await api.post(`/load-sample/${datasetId}`)
  return data
}
