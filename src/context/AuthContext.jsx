import { createContext, useContext, useMemo, useState } from 'react'
import { api } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('aic_user') || 'null') } catch { return null }
  })

  const login = async (email, password) => {
    const result = await api.login({ email, password })
    localStorage.setItem('aic_access_token', result.access_token)
    localStorage.setItem('aic_user', JSON.stringify(result.user))
    setUser(result.user)
    return result
  }

  const register = (payload) => api.register(payload)

  const logout = () => {
    localStorage.removeItem('aic_access_token')
    localStorage.removeItem('aic_user')
    setUser(null)
  }

  const value = useMemo(() => ({ user, login, register, logout, isAuthenticated: !!localStorage.getItem('aic_access_token') }), [user])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
