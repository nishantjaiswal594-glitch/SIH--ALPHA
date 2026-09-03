import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowRight, BriefcaseBusiness, CheckCircle2, Eye, EyeOff, GraduationCap,
  LockKeyhole, Network, ShieldCheck, Sparkles, Target, Users, Zap
} from 'lucide-react';
import './styles/global.css';

const features = [
  { icon: Target, title: 'Skill Mapping', text: 'Build a strong profile of your skills and competencies.' },
  { icon: Network, title: 'Identify Gaps', text: 'Discover skill gaps and get personalized learning recommendations.' },
  { icon: BriefcaseBusiness, title: 'Match & Connect', text: 'Find internships and job opportunities that match your potential.' },
];

const ecosystems = [
  { icon: GraduationCap, title: 'Students', text: 'Build Skills', tone: 'student' },
  { icon: GraduationCap, title: 'Academia', text: 'Nurture Talent', tone: 'academia' },
  { icon: BriefcaseBusiness, title: 'Industry', text: 'Hire & Innovate', tone: 'industry' },
];

function BrandMark() {
  return (
    <div className="brand-mark">
      <div className="brand-symbol" aria-hidden="true"><span /><span /><span /></div>
      <div>
        <strong>SkillBridge</strong>
        <small>Academia • Industry • Students</small>
      </div>
    </div>
  );
}

function EcosystemCard({ className, icon: Icon, title, lines, tone }) {
  return (
    <div className={`ecosystem-card ${className} ${tone}`}>
      <div className="ecosystem-card-icon"><Icon size={22} /></div>
      <strong>{title}</strong>
      {lines.map((line) => <span key={line}>{line}</span>)}
    </div>
  );
}

function SkillProfile() {
  return (
    <div className="profile-visual" aria-label="Skill Profile connecting students, academia, industry and opportunities">
      <div className="node-line line-student" />
      <div className="node-line line-academia" />
      <div className="node-line line-industry" />
      <div className="node-line line-opportunity" />
      <div className="node-dot dot-student" />
      <div className="node-dot dot-academia" />
      <div className="node-dot dot-industry" />
      <div className="node-dot dot-opportunity" />

      <EcosystemCard className="student-card" icon={GraduationCap} title="Students" lines={['Build your skills', 'Build your future']} tone="student" />
      <EcosystemCard className="academia-card" icon={GraduationCap} title="Academia" lines={['Guide • Educate', '• Empower']} tone="academia" />
      <EcosystemCard className="industry-card" icon={BriefcaseBusiness} title="Industry" lines={['Find Talent', 'Drive Innovation']} tone="industry" />
      <EcosystemCard className="opportunity-card" icon={Sparkles} title="Opportunities" lines={['Internships', 'Placements • Careers']} tone="opportunity" />

      <div className="skill-hex" aria-hidden="true">
        <div className="hex-inner"><strong>Skill<br />Profile</strong></div>
      </div>
    </div>
  );
}

function BrandPanel() {
  return (
    <section className="brand-panel">
      <div className="brand-top"><BrandMark /></div>
      <div className="decor-dots dots-top" aria-hidden="true" />
      <div className="decor-dots dots-bottom" aria-hidden="true" />

      <div className="hero-copy">
        <h1>Turn Skills into<br /><em>Opportunities</em></h1>
        <p>Bridge the gap between what you know<br className="desktop-only" /> and what the world needs.</p>
      </div>

      <div className="feature-list">
        {features.map(({ icon: Icon, title, text }) => (
          <div className="feature" key={title}>
            <div className="feature-icon"><Icon size={20} /></div>
            <div><strong>{title}</strong><span>{text}</span></div>
          </div>
        ))}
      </div>

      <SkillProfile />

      <div className="ai-card">
        <div className="ai-icon"><Sparkles size={21} /></div>
        <div><strong>AI-Powered Matching</strong><span>Intelligent insights for better outcomes</span></div>
      </div>
    </section>
  );
}

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = (event) => {
    event.preventDefault();
    setStatus('');
    if (!/^\S+@\S+\.\S+$/.test(email.trim())) {
      setStatus('Please enter a valid email address.');
      return;
    }
    if (password.length < 6) {
      setStatus('Password must be at least 6 characters.');
      return;
    }
    setLoading(true);
    window.setTimeout(() => {
      setLoading(false);
      setStatus('Sign-in is ready for your authentication API.');
    }, 550);
  };

  return (
    <section className="login-panel">
      <div className="account-prompt">New here? <button type="button" onClick={() => setStatus('Account creation will open here.')}>Create an account</button></div>
      <div className="login-content">
        <div className="login-heading">
          <div className="welcome-icon"><Users size={30} /></div>
          <h2>Welcome back!</h2>
          <p>Sign in to access your SkillBridge dashboard.</p>
        </div>

        <form onSubmit={submit} noValidate>
          <label>Email address
            <div className="input-wrap"><span className="input-icon">✉</span><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Enter your email" autoComplete="email" /></div>
          </label>
          <label>Password
            <div className="input-wrap password-wrap"><span className="input-icon">▢</span><input type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter your password" autoComplete="current-password" /><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword((value) => !value)}>{showPassword ? <EyeOff size={20} /> : <Eye size={20} />}</button></div>
          </label>

          <div className="form-options">
            <label className="remember"><input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} /><span>Remember me</span></label>
            <button type="button" className="link-button" onClick={() => setStatus('Password recovery will open here.')}>Forgot password?</button>
          </div>

          <button className="primary-button" type="submit" disabled={loading}>{loading ? 'Signing In…' : 'Sign In'} <ArrowRight size={21} /></button>
          <div className="divider"><span>or continue with</span></div>
          <button type="button" className="google-button" onClick={() => setStatus('Google authentication is ready for OAuth integration.')}><span className="google-g">G</span>Continue with Google</button>
          {status && <div className="form-status" role="status"><CheckCircle2 size={17} />{status}</div>}
        </form>

        <div className="security-note">
          <div className="security-icon"><ShieldCheck size={28} /></div>
          <div><strong>Secure &amp; Trusted</strong><span>Your data is protected with enterprise-grade<br className="desktop-only" /> security and privacy.</span></div>
        </div>
      </div>
    </section>
  );
}

function EcosystemFooter() {
  return (
    <section className="ecosystem-footer">
      <h3>One Platform. Three Ecosystems. One Shared Goal.</h3>
      <div className="ecosystem-grid">
        {ecosystems.map(({ icon: Icon, title, text, tone }, index) => (
          <React.Fragment key={title}>
            <div className={`eco-item ${tone}`}><div className="eco-icon"><Icon size={24} /></div><div><strong>{title}</strong><span>{text}</span></div></div>
            {index < 2 && <div className="eco-arrow"><span>←</span><span>→</span></div>}
          </React.Fragment>
        ))}
      </div>
    </section>
  );
}

function App() {
  return <main className="page"><div className="app-shell"><div className="main-grid"><BrandPanel /><LoginForm /></div><EcosystemFooter /></div></main>;
}

createRoot(document.getElementById('root')).render(<App />);
