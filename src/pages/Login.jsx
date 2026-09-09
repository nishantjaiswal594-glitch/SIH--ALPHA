import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ShieldCheck, Sparkles } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth(); const navigate = useNavigate(); const location = useLocation()
  const [email, setEmail] = useState(''); const [password, setPassword] = useState(''); const [error, setError] = useState(''); const [loading, setLoading] = useState(false)
  const submit = async (e) => { e.preventDefault(); setError(''); setLoading(true); try { await login(email, password); navigate(location.state?.from || '/student') } catch (e) { setError(e.message) } finally { setLoading(false) } }
  return <AuthShell><div className="auth-card"><div className="auth-title"><Sparkles size={18}/><span>Student access</span></div><h1>Welcome <span>back.</span></h1><p>Sign in to continue your skill-to-career journey.</p>{error && <div className="error-box">{error}</div>}<form onSubmit={submit}><label>Email<input value={email} onChange={e=>setEmail(e.target.value)} type="email" required /></label><label>Password<input value={password} onChange={e=>setPassword(e.target.value)} type="password" required /></label><div className="row-between"><Link to="/forgot-password">Forgot password?</Link></div><button className="btn-primary full" disabled={loading}>{loading?'Signing in…':'Sign in'}<span>→</span></button></form><div className="auth-foot">New here? <Link to="/register">Create an account</Link></div></div></AuthShell>
}
function AuthShell({children}) { return <div className="auth-shell"><div className="auth-ambient"><div className="orb orb-a"/><div className="orb orb-b"/><div className="auth-brand"><div className="brand-mark">A</div><div><div className="brand-name">AIC Portal</div><div className="brand-sub">AI • Academia • Industry</div></div></div><div className="auth-pitch"><span>Measure.</span><span>Understand.</span><span>Move forward.</span><small>Your skill intelligence platform for the next opportunity.</small></div></div>{children}<div className="auth-safe"><ShieldCheck size={15}/> Secure API-backed workspace</div></div> }
