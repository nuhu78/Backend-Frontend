import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { apiRequest, clearSession, getAccessToken, setSession } from '../lib/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const bootstrap = async () => {
      const token = getAccessToken()

      if (!token) {
        setLoading(false)
        return
      }

      try {
        const profile = await apiRequest('/auth/profile/')
        setUser(profile)
      } catch {
        clearSession()
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    bootstrap()
  }, [])

  async function signIn({ identifier, password }) {
    const data = await apiRequest('/auth/login/', {
      method: 'POST',
      auth: false,
      body: { identifier, password },
    })

    setSession(data.tokens)
    setUser(data.user)
    return data
  }

  async function signUp(payload) {
    const data = await apiRequest('/auth/register/', {
      method: 'POST',
      auth: false,
      body: payload,
    })

    setSession(data.tokens)
    setUser(data.user)
    return data
  }

  async function signOut() {
    const refresh = window.localStorage.getItem('lms_refresh_token')

    try {
      if (refresh) {
        await apiRequest('/auth/logout/', {
          method: 'POST',
          body: { refresh },
        })
      }
    } catch {
      // Ignore logout failures and clear local session.
    } finally {
      clearSession()
      setUser(null)
    }
  }

  async function refreshProfile() {
    const profile = await apiRequest('/auth/profile/')
    setUser(profile)
    return profile
  }

  async function updateProfile(payload) {
    const data = await apiRequest('/auth/profile/', {
      method: 'PUT',
      body: payload,
    })

    setUser(data.user)
    return data
  }

  async function forgotPassword(email) {
    return apiRequest('/auth/forgot-password/', {
      method: 'POST',
      auth: false,
      body: { email },
    })
  }

  async function resetPassword(payload) {
    return apiRequest('/auth/reset-password/', {
      method: 'POST',
      auth: false,
      body: payload,
    })
  }

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      signIn,
      signUp,
      signOut,
      refreshProfile,
      updateProfile,
      forgotPassword,
      resetPassword,
    }),
    [user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }

  return context
}
