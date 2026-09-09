const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem('aic_access_token')
  const headers = new Headers(options.headers || {})
  // FastAPI/Pydantic needs an explicit JSON content type for stringified JSON bodies.
  // Most API helpers below pass JSON.stringify(...) strings, so checking for
  // non-string bodies caused requests such as /auth/login to arrive without
  // Content-Type and be rejected by the backend with a Pydantic validation error.
  if (!headers.has('Content-Type') && options.body != null) {
    headers.set('Content-Type', 'application/json')
  }
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })
  const contentType = response.headers.get('content-type') || ''
  const payload = contentType.includes('application/json') ? await response.json() : await response.text()

  if (!response.ok) {
    const detail = typeof payload === 'object' && payload?.detail ? payload.detail : `Request failed (${response.status})`
    const error = new Error(Array.isArray(detail) ? detail.map((x) => x.msg || JSON.stringify(x)).join(', ') : detail)
    error.status = response.status
    error.payload = payload
    throw error
  }
  return payload
}

export const api = {
  login: (body) => apiFetch('/auth/login', { method: 'POST', body: JSON.stringify(body) }),
  register: (body) => apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(body) }),
  forgotPassword: (body) => apiFetch('/auth/forgot-password', { method: 'POST', body: JSON.stringify(body) }),
  resetPassword: (body) => apiFetch('/auth/reset-password', { method: 'POST', body: JSON.stringify(body) }),
  verifyEmail: (token) => apiFetch(`/auth/verify-email?token=${encodeURIComponent(token)}`),
  googleLogin: (credential) => apiFetch('/auth/google', { method: 'POST', body: JSON.stringify({ credential }) }),
  me: () => apiFetch('/users/me'),
  profile: () => apiFetch('/users/me/profile'),
  updateProfile: (body) => apiFetch('/users/me/profile', { method: 'PUT', body: JSON.stringify(body) }),
  skills: () => apiFetch('/users/me/skills'),
  addSkill: (skillId, proficiencyLevel) => apiFetch(`/users/me/skills?skill_id=${encodeURIComponent(skillId)}&proficiency_level=${encodeURIComponent(proficiencyLevel)}`, { method: 'POST' }),
  deleteSkill: (skillId) => apiFetch(`/users/me/skills/${skillId}`, { method: 'DELETE' }),
  projects: () => apiFetch('/users/me/projects'),
  addProject: (title) => apiFetch(`/users/me/projects?title=${encodeURIComponent(title)}`, { method: 'POST' }),
  deleteProject: (projectId) => apiFetch(`/users/me/projects/${projectId}`, { method: 'DELETE' }),
  assessment: () => apiFetch('/assessment/current'),
  submitAssessment: (body) => apiFetch('/assessment/submit', { method: 'POST', body: JSON.stringify(body) }),
  assessmentResult: () => apiFetch('/assessment/result'),
  skillAnalysis: () => apiFetch('/skills/analysis'),
  skillGaps: () => apiFetch('/skills/gaps'),
  recommendedOpportunity: () => apiFetch('/opportunities/recommended'),
  opportunityCompatibility: (id) => apiFetch(`/opportunities/${id}/compatibility`),
  apply: (id) => apiFetch(`/opportunities/${id}/apply`, { method: 'POST' })
}
