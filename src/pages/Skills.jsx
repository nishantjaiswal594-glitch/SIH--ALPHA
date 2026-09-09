import { useCallback, useEffect, useState } from 'react'
import { api } from '../api/client'
import { ArrowRight, Brain, CheckCircle2, Target, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Skills() {
  const [data, setData] = useState(null)
  const [gaps, setGaps] = useState(null)
  const [skills, setSkills] = useState(null)
  const [projects, setProjects] = useState(null)
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState([])

  const load = useCallback(async () => {
    setLoading(true)
    setErrors([])
    const results = await Promise.allSettled([
      api.skillAnalysis(),
      api.skillGaps(),
      api.skills(),
      api.projects(),
    ])

    const [analysis, gapResult, skillResult, projectResult] = results
    if (analysis.status === 'fulfilled') setData(analysis.value || {})
    else setData(null)
    if (gapResult.status === 'fulfilled') setGaps(gapResult.value || {})
    if (skillResult.status === 'fulfilled') setSkills(skillResult.value || { skills: [] })
    if (projectResult.status === 'fulfilled') setProjects(projectResult.value || { projects: [] })

    setErrors(results.filter(x => x.status === 'rejected').map(x => x.reason?.message || 'A backend request failed.'))
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  if (loading) return <div className="loading-screen"><div className="spinner" />Analyzing skill signals…</div>

  if (!data) {
    return (
      <div className="error-page">
        <div className="error-box">{errors[0] || 'No skill analysis is available yet. Complete the assessment first.'}</div>
        <div className="error-actions">
          <Link className="btn-primary" to="/student/assessment">Take assessment <ArrowRight size={15} /></Link>
          <button className="btn-secondary" onClick={load}>Retry</button>
        </div>
      </div>
    )
  }

  const cats = Array.isArray(data.skills) ? data.skills : []
  const score = Number.isFinite(Number(data.overall_score)) ? Number(data.overall_score) : 0
  const skillItems = Array.isArray(skills?.skills) ? skills.skills : []
  const projectItems = Array.isArray(projects?.projects) ? projects.projects : []
  const gapItems = Array.isArray(gaps?.gaps) ? gaps.gaps : []

  return (
    <div>
      <div className="page-kicker">SKILL PROFILE</div>
      <div className="title-row">
        <div><h1>Know where you <span>stand.</span></h1><p>Your latest assessment translated into measurable skill signals.</p></div>
        <Link className="btn-primary" to="/student/assessment">Retake assessment <ArrowRight size={15} /></Link>
      </div>

      {errors.length > 0 && <div className="warning-box">Some optional skill data is unavailable: {errors[0]}</div>}

      <div className="skill-hero">
        <div className="score-ring" style={{ '--score': `${score}%` }}>
          <div><strong>{score}%</strong><span>overall score</span></div>
        </div>
        <div>
          <div className="eyebrow"><TrendingUp size={14} /> Current assessment</div>
          <h2>{score >= 80 ? 'You’re on the right track.' : score >= 60 ? 'Good progress—keep building.' : 'Your next step is clear.'}</h2>
          <p>Scores are calculated by the backend from your latest submitted assessment.</p>
          <div className="chips">{cats.map(x => <span key={x.skill}>{x.skill} • {x.score}%</span>)}</div>
        </div>
      </div>

      <div className="grid-2">
        <Panel title="Skill distribution" icon={Brain}>
          {cats.length ? <div className="bars">{cats.map(x => {
            const value = Math.max(0, Math.min(100, Number(x.score) || 0))
            return <div className="bar-row" key={x.skill}>
              <div><span>{x.skill}</span><strong>{value}%</strong></div>
              <div className="bar"><i style={{ width: `${value}%` }} /></div>
              <small>{x.level || '—'} • {x.status || '—'}</small>
            </div>
          })}</div> : <div className="empty">No category scores were returned.</div>}
        </Panel>

        <Panel title="Skill gaps" icon={Target}>
          {gapItems.length ? <div className="gap-list">{gapItems.map(g => <div className="gap-row" key={g.skill}>
            <div><strong>{g.skill}</strong><span>{g.current_score}% → {g.required_score}% required</span></div>
            <em className={`priority ${String(g.priority || 'low').toLowerCase()}`}>{g.priority || 'Low'}</em>
          </div>)}</div> : <div className="empty"><CheckCircle2 size={19} /> No skill gaps at the 70% threshold.</div>}
        </Panel>
      </div>

      <div className="grid-2">
        <Panel title="Your added skills">
          {skillItems.length ? <div className="skill-pills">{skillItems.map(s => <span key={s.skill_id}><strong>{s.skill_name}</strong><small>{s.category || '—'} • {s.proficiency_level || '—'}</small></span>)}</div> : <div className="empty">No skills added to your profile yet. The backend currently requires a skill ID to add one.</div>}
        </Panel>
        <Panel title="Projects">
          {projectItems.length ? <div className="project-list">{projectItems.map(p => <div className="list-row" key={p.project_id}><div><strong>{p.title || 'Untitled project'}</strong><span>Stored as project title only in the current API.</span></div></div>)}</div> : <div className="empty">No projects added yet.</div>}
        </Panel>
      </div>
    </div>
  )
}

const Panel = ({ title, icon: Icon, children }) => <section className="panel"><div className="panel-head"><div className="panel-title">{Icon && <Icon size={16} />}<h2>{title}</h2></div></div>{children}</section>
