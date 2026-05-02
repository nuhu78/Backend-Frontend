const API_BASE = '/api'
const ACCESS_TOKEN_KEY = 'lms_access_token'
const REFRESH_TOKEN_KEY = 'lms_refresh_token'

export function getAccessToken() {
  return window.localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function getRefreshToken() {
  return window.localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setSession(tokens) {
  if (tokens?.access) {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access)
  }

  if (tokens?.refresh) {
    window.localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh)
  }
}

export function clearSession() {
  window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  window.localStorage.removeItem(REFRESH_TOKEN_KEY)
}

async function refreshAccessToken() {
  const refresh = getRefreshToken()

  if (!refresh) {
    return null
  }

  const response = await fetch(`${API_BASE}/auth/token/refresh/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh }),
  })

  if (!response.ok) {
    clearSession()
    return null
  }

  const data = await response.json()
  setSession({ access: data.access, refresh })
  return data.access
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || ''
  const payload = contentType.includes('application/json') ? await response.json() : null

  if (!response.ok) {
    const detail = payload?.detail || payload?.error || payload || 'Request failed'
    throw new Error(typeof detail === 'string' ? detail : 'Request failed')
  }

  return payload
}

export async function apiRequest(path, options = {}) {
  const {
    method = 'GET',
    body,
    auth = true,
    retry = true,
    headers = {},
  } = options

  const requestHeaders = {
    'Content-Type': 'application/json',
    ...headers,
  }

  if (auth) {
    const access = getAccessToken()
    if (access) {
      requestHeaders.Authorization = `Bearer ${access}`
    }
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
  })

  if (response.status === 401 && auth && retry) {
    const refreshed = await refreshAccessToken()

    if (refreshed) {
      return apiRequest(path, { ...options, retry: false })
    }
  }

  return parseResponse(response)
}
