import React, {useState} from 'react';
import { createRoot } from 'react-dom/client';
import { Eye, EyeOff, GraduationCap, Building2, Users, BriefcaseBusiness, Sparkles, ArrowRight, CheckCircle2, LockKeyhole, Network, Target, Zap, ShieldCheck } from 'lucide-react';
import './styles/global.css';

const features = [
  {icon: Target, title:'Skill Mapping', text:'Build a clear picture of what you know and where you can grow.'},
  {icon: Zap, title:'Identify Gaps', text:'Turn skill gaps into focused, actionable learning opportunities.'},
  {icon: Network, title:'Match & Connect', text:'Create meaningful connections between talent and opportunity.'}
];

const ecosystems = [
  {icon: Users, title:'Students', text:'Discover your strengths, build skills and find your next opportunity.'},
  {icon: GraduationCap, title:'Academia', text:'Connect learning outcomes with the skills industry needs.'},
  {icon: Building2, title:'Industry', text:'Find relevant talent and shape the future workforce.'}
];

function BrandMark(){return <div className="brand-mark"><div className="brand-symbol"><span/><span/><span/></div><div><strong>SkillBridge</strong><small>Connecting Skills to Opportunities</small></div></div>}

function SkillProfile(){return <div className="profile-visual" aria-label="Skill profile illustration">
  <div className="orbit orbit-a"/><div className="orbit orbit-b"/>
  <div className="profile-core"><div className="avatar"><Users size={25}/></div><strong>Skill Profile</strong><span>AI-powered insight</span><div className="skill-bars"><i/><i/><i/></div></div>
  <div className="float-card card-student"><Users size={15}/><span>Students</span></div>
  <div className="float-card card-academia"><GraduationCap size={15}/><span>Academia</span></div>
  <div className="float-card card-industry"><Building2 size={15}/><span>Industry</span></div>
  <div className="connection c1"/><div className="connection c2"/><div className="connection c3"/>
</div>}

function BrandPanel(){return <section className="brand-panel">
  <div className="brand-top"><BrandMark/><span className="mini-pill"><Sparkles size={12}/> AI-powered</span></div>
  <div className="hero-copy"><p className="eyebrow">ACADEMIA <b>•</b> INDUSTRY <b>•</b> STUDENTS</p><h1>Turn Skills into <em>Opportunities.</em></h1><p>SkillBridge creates a connected ecosystem where skills become visible, gaps become actionable, and people meet the opportunities built for them.</p></div>
  <div className="feature-list">{features.map(({icon:Icon,title,text})=><div className="feature" key={title}><div className="feature-icon"><Icon size={17}/></div><div><strong>{title}</strong><span>{text}</span></div></div>)}</div>
  <SkillProfile/>
  <div className="ai-card"><div className="ai-icon"><Sparkles size={17}/></div><div><strong>AI-Powered Matching</strong><span>Smarter connections. Better outcomes.</span></div><ArrowRight size={17}/></div>
</section>}

function LoginForm(){
 const [showPassword,setShowPassword]=useState(false); const [remember,setRemember]=useState(false); const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const [status,setStatus]=useState('');
 const submit=(e)=>{e.preventDefault(); setStatus(''); if(!/^\S+@\S+\.\S+$/.test(email)){setStatus('Please enter a valid email address.');return} if(password.length<6){setStatus('Password must be at least 6 characters.');return} setStatus('Ready to connect to your authentication API.');};
 return <section className="login-panel">
   <div className="account-prompt">New here? <button type="button" onClick={()=>setStatus('Account creation will open here.')}>Create an account <ArrowRight size={14}/></button></div>
   <div className="login-content"><div className="login-heading"><div className="welcome-icon"><Users size={20}/></div><span>WELCOME BACK</span><h2>Sign in to SkillBridge</h2><p>Continue building your path from skills to opportunities.</p></div>
   <form onSubmit={submit} noValidate>
    <label>Email address<input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" autoComplete="email"/></label>
    <label>Password<div className="password-wrap"><input type={showPassword?'text':'password'} value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter your password" autoComplete="current-password"/><button type="button" aria-label={showPassword?'Hide password':'Show password'} onClick={()=>setShowPassword(v=>!v)}>{showPassword?<EyeOff size={18}/>:<Eye size={18}/>}</button></div></label>
    <div className="form-options"><label className="remember"><input type="checkbox" checked={remember} onChange={e=>setRemember(e.target.checked)}/><span>Remember me</span></label><button type="button" className="link-button" onClick={()=>setStatus('Password recovery will open here.')}>Forgot password?</button></div>
    <button className="primary-button" type="submit">Sign In <ArrowRight size={17}/></button>
    <div className="divider"><span>or continue with</span></div>
    <button type="button" className="google-button" onClick={()=>setStatus('Google authentication is ready for OAuth integration.')}><span className="google-g">G</span>Continue with Google</button>
    {status && <div className="form-status" role="status"><CheckCircle2 size={16}/>{status}</div>}
   </form>
   <div className="security-note"><ShieldCheck size={20}/><div><strong>Secure & Trusted</strong><span>Your information is protected with secure authentication and privacy-first practices.</span></div></div>
   </div>
 </section>
}

function EcosystemFooter(){return <section className="ecosystem-footer"><div className="footer-heading"><span>THE SKILLBRIDGE ECOSYSTEM</span><h3>One Platform. <em>Three Ecosystems.</em> One Shared Goal.</h3></div><div className="ecosystem-grid">{ecosystems.map(({icon:Icon,title,text},i)=><React.Fragment key={title}><div className="eco-item"><div className="eco-icon"><Icon size={19}/></div><div><strong>{title}</strong><span>{text}</span></div></div>{i<2&&<div className="eco-arrow">↔</div>}</React.Fragment>)}</div></section>}

function App(){return <main className="page"><div className="app-shell"><div className="main-grid"><BrandPanel/><LoginForm/></div><EcosystemFooter/></div><p className="page-foot"><LockKeyhole size={12}/> Built for meaningful skill-to-opportunity connections</p></main>}
createRoot(document.getElementById('root')).render(<App/>);
