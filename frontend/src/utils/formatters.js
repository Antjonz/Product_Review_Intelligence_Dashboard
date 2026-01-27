export function formatNumber(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return String(n)
}

export function sentimentColor(sentiment) {
  if (sentiment === 'positive') return '#10b981'
  if (sentiment === 'negative') return '#ef4444'
  return '#6b7280'
}

export function ratingStars(rating) {
  return '\u2605'.repeat(Math.round(rating)) + '\u2606'.repeat(5 - Math.round(rating))
}

export function truncate(str, len = 100) {
  if (!str) return ''
  return str.length > len ? str.slice(0, len) + '...' : str
}
