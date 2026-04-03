const rawBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

export const API_BASE_URL = rawBaseUrl
  ? rawBaseUrl.replace(/\/$/, '')
  : 'http://127.0.0.1:8000'

export function apiUrl(path: string) {
  return `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
}
