import { useCallback, useEffect, useState } from 'react'
import { api } from '../api/client'
import { ArrowRight, Edit3, Mail, MapPin, Phone, Save, Trash2, UserRound, X } from 'lucide-react'

const EMPTY_PROFILE = {
  personal: {},
  academic: {},
  career: {},
  profile: {},
  statistics: { skills_added: 0, applications: 0, projects: 0, internships: null },
}

export default function Profile() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [edit, setEdit] = useState(false)
  const [form, setForm] = useState({})
  const [msg, setMsg] = useState('')
  const [error, setError] = useState('')
  const [project, setProject] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const response = await api.profile()
      const safe = {
        ...EMPTY_PROFILE,
        ...(response || {}),
        personal: { ...EMPTY_PROFILE.personal, ...(response?.personal || {}) },
        academic: { ...EMPTY_PROFILE.academic, ...(response?.academic || {}) },
        career: { ...EMPTY_PROFILE.career, ...(response?.career || {}) },
        profile: { ...EMPTY_PROFILE.profile, ...(response?.profile || {}) },
        statistics: { ...EMPTY_PROFILE.statistics, ...(response?.statistics || {}) },
      }
      setData(safe)
      setForm({ ...safe.personal, ...safe.academic, ...safe.career })
    } catch (e) {
      setData(null)
      setError(e?.message || 'Unable to load your profile.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  if (loading) return <Loading />

  if (!data) {
    return (
      <div className="error-page">
        <div className="error-box">{error || 'Unable to load your profile.'}</div>
        <button className="btn-primary" onClick={load}>Retry <ArrowRight size={15} /></button>
      </div>
    )
  }

  const p = data.personal || {}
  const a = data.academic || {}
  const c = data.career || {}
  const s = data.statistics || EMPTY_PROFILE.statistics

  const update = async (event) => {
    event.preventDefault()
    setError('')
    setMsg('')
    try {
      const body = { ...form }
      delete body.id
      delete body.email
      delete body.role
      delete body.is_verified
      delete body.student_id
      delete body.profile_picture_url
      delete body.resume_url
      if (body.graduation_year !== '' && body.graduation_year != null) body.graduation_year = Number(body.graduation_year)
      if (body.semester !== '' && body.semester != null) body.semester = Number(body.semester)
      if (body.cgpa !== '' && body.cgpa != null) body.cgpa = Number(body.cgpa)
      await api.updateProfile(body)
      setMsg('Profile updated successfully.')
      setEdit(false)
      await load()
    } catch (e) {
      setError(e?.message || 'Unable to update your profile.')
    }
  }

  const addProject = async (event) => {
    event.preventDefault()
    if (!project.trim()) return
    setError('')
    try {
      await api.addProject(project.trim())
      setProject('')
      await load()
    } catch (e) {
      setError(e?.message || 'Unable to add project.')
    }
  }

  return (
    <div>
      <Kicker>STUDENT PROFILE</Kicker>
      <div className="profile-hero">
        <div className="profile-id">
          <div className="avatar avatar-xl">{(p.name || 'S').slice(0, 1).toUpperCase()}</div>
          <div>
            <h1>{p.name || 'Student'}</h1>
            <p>{a.degree || 'Student'} {a.branch ? `• ${a.branch}` : ''}</p>
            <div className="chips">
              <span>{a.college || 'College not set'}</span>
              {p.location && <span><MapPin size={12} />{p.location}</span>}
            </div>
          </div>
        </div>
        <button className="btn-secondary" onClick={() => { setMsg(''); setEdit(true) }}><Edit3 size={15} /> Edit profile</button>
      </div>

      {error && <div className="error-box">{error}</div>}
      {msg && <div className="success-box">{msg}</div>}

      <div className="metric-grid four">
        <Metric label="Skills" value={s.skills_added ?? 0} />
        <Metric label="Projects" value={s.projects ?? 0} />
        <Metric label="Applications" value={s.applications ?? 0} />
        <Metric label="Internships" value={s.internships ?? '—'} />
      </div>

      <div className="grid-2">
        <Panel title="Personal information">
          <Info label="Email" value={p.email} icon={Mail} />
          <Info label="Phone" value={p.phone || 'Not provided'} icon={Phone} />
          <Info label="Location" value={p.location || 'Not provided'} icon={MapPin} />
          <Info label="Date of birth" value={p.date_of_birth || 'Not provided'} icon={UserRound} />
        </Panel>
        <Panel title="Academic information">
          <Info label="Student ID" value={a.student_id} />
          <Info label="College" value={a.college} />
          <Info label="Degree" value={a.degree} />
          <Info label="Branch" value={a.branch} />
          <Info label="Graduation year" value={a.graduation_year} />
          <Info label="Semester" value={a.semester} />
          <Info label="CGPA" value={a.cgpa} />
        </Panel>
      </div>

      <div className="grid-2">
        <Panel title="Career interests">
          <div className="pref-list">
            <Pref label="Preferred roles" value={c.preferred_roles} />
            <Pref label="Industries" value={c.preferred_industries} />
            <Pref label="Work locations" value={c.preferred_work_locations} />
          </div>
        </Panel>
        <Projects onError={setError} />
      </div>

      {edit && <EditModal form={form} setForm={setForm} onClose={() => setEdit(false)} onSubmit={update} />}

      <form onSubmit={addProject} className="add-project">
        <input placeholder="Add a project title…" value={project} onChange={e => setProject(e.target.value)} />
        <button className="btn-primary"><Save size={15} /> Add project</button>
      </form>
    </div>
  )
}

function Projects({ onError }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setData(await api.projects())
    } catch (e) {
      setData({ projects: [] })
      onError(e?.message || 'Unable to load projects.')
    } finally {
      setLoading(false)
    }
  }, [onError])

  useEffect(() => { load() }, [load])

  const del = async (id) => {
    try {
      await api.deleteProject(id)
      await load()
    } catch (e) {
      onError(e?.message || 'Unable to delete project.')
    }
  }

  return (
    <Panel title="Projects">
      <div className="project-list">
        {loading ? <div className="empty">Loading projects…</div> : data?.projects?.length ? data.projects.map(x => (
          <div className="list-row" key={x.project_id}>
            <div><strong>{x.title || 'Untitled project'}</strong><span>Project title stored in backend</span></div>
            <button type="button" className="icon-btn danger" onClick={() => del(x.project_id)}><Trash2 size={15} /></button>
          </div>
        )) : <div className="empty">No projects found.</div>}
      </div>
    </Panel>
  )
}

const EditModal = ({ form, setForm, onClose, onSubmit }) => (
  <div className="modal-backdrop">
    <div className="modal">
      <button className="modal-close" onClick={onClose}><X size={18} /></button>
      <h2>Edit profile</h2>
      <p>Only fields accepted by <code>PUT /users/me/profile</code> are shown.</p>
      <form onSubmit={onSubmit} className="form-grid">
        {['name', 'phone', 'date_of_birth', 'location', 'college', 'degree', 'branch', 'graduation_year', 'semester', 'cgpa', 'preferred_roles', 'preferred_industries', 'preferred_work_locations'].map(k => (
          <label key={k}>
            {k.replaceAll('_', ' ')}
            <input
              type={k === 'date_of_birth' ? 'date' : k === 'graduation_year' || k === 'semester' || k === 'cgpa' ? 'number' : 'text'}
              step={k === 'cgpa' ? '0.01' : undefined}
              value={form[k] ?? ''}
              onChange={e => setForm({ ...form, [k]: e.target.value })}
            />
          </label>
        ))}
        <button className="btn-primary" type="submit">Save changes <ArrowRight size={15} /></button>
      </form>
    </div>
  </div>
)

const Info = ({ label, value, icon: Icon }) => (
  <div className="info-row">
    <div className="mini-icon">{Icon ? <Icon size={14} /> : null}</div>
    <div><span>{label}</span><strong>{value ?? '—'}</strong></div>
  </div>
)

const Pref = ({ label, value }) => (
  <div className="pref">
    <span>{label}</span>
    <div>{String(value || 'Not set').split(',').filter(Boolean).map(v => <em key={v.trim()}>{v.trim()}</em>)}</div>
  </div>
)

const Metric = ({ label, value }) => <div className="metric-card"><span>{label}</span><strong>{value}</strong></div>
const Panel = ({ title, children }) => <section className="panel"><div className="panel-head"><h2>{title}</h2></div>{children}</section>
const Kicker = ({ children }) => <div className="page-kicker">{children}</div>
const Loading = () => <div className="loading-screen"><div className="spinner" />Loading profile…</div>
