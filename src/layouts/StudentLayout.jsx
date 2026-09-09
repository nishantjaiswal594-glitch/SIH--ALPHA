import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { Bell, BriefcaseBusiness, ChevronRight, FileText, GraduationCap, LayoutDashboard, LogOut, Menu, PanelLeft, Search, Settings, Sparkles, UserRound, X } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useState } from 'react'

const nav = [
  ['/student', LayoutDashboard, 'Dashboard'],
  ['/student/profile', UserRound, 'My Profile'],
  ['/student/assessment', GraduationCap, 'Skill Assessment'],
  ['/student/skills', Sparkles, 'Skill Profile'],
  ['/student/career', BriefcaseBusiness, 'Career Path'],
  ['/student/learning', Sparkles, 'Learning'],
  ['/student/opportunities', BriefcaseBusiness, 'Opportunities'],
  ['/student/applications', FileText, 'Applications'],
  ['/student/portfolio', FileText, 'Digital Portfolio'],
  ['/student/settings', Settings, 'Settings']
]

export default function StudentLayout() {
  const { user, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()
  return <div className="app-shell">
    <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}>
      <div className="brand"><div className="brand-mark">A</div><div><div className="brand-name">AIC Portal</div><div className="brand-sub">AI • Academia • Industry</div></div><button className="mobile-close" onClick={() => setOpen(false)}><X size={18}/></button></div>
      <nav>
        {nav.map(([to, Icon, label]) => <NavLink key={to} to={to} end={to === '/student'} onClick={() => setOpen(false)} className={({isActive}) => `nav-item ${isActive ? 'active' : ''}`}><Icon size={16}/><span>{label}</span></NavLink>)}
      </nav>
      <div className="sidebar-card"><Sparkles size={22}/><strong>Build your future.</strong><span>Turn skill data into career actions.</span></div>
      <button className="nav-item logout" onClick={() => { logout(); navigate('/login') }}><LogOut size={16}/><span>Sign out</span></button>
    </aside>
    <main className="main-content">
      <header className="topbar"><button className="mobile-menu" onClick={() => setOpen(true)}><Menu size={19}/></button><div className="search"><Search size={15}/><input placeholder="Search opportunities, courses, or skills..." /></div><div className="top-actions"><button className="icon-btn"><Bell size={17}/><span className="notification-dot"/></button><button className="profile-chip" onClick={() => navigate('/student/profile')}><span className="avatar avatar-sm">{(user?.name || 'S').slice(0,1).toUpperCase()}</span><span className="profile-chip-name">{user?.name || 'Student'}</span><ChevronRight size={14}/></button></div></header>
      <section className="page-wrap"><Outlet /></section>
    </main>
  </div>
}
