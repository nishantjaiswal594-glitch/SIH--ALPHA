# Backend synchronization matrix

| Frontend surface | Backend source | Sync state |
|---|---|---|
| Login/Register | `/auth/login`, `/auth/register` | Live |
| Verify email | `/auth/verify-email` | Live |
| Password reset | `/auth/forgot-password`, `/auth/reset-password` | Live |
| Student profile | `/users/me/profile` GET/PUT | Live |
| Projects | `/users/me/projects` GET/POST/DELETE | Live; title-only API |
| Skills | `/users/me/skills` GET/POST/DELETE | Live; POST requires skill_id + proficiency_level query params |
| Skill assessment | `/assessment/current`, `/assessment/submit` | Live |
| Assessment result | `/assessment/result` | Live |
| Skill analysis | `/skills/analysis` | Live |
| Skill gaps | `/skills/gaps` | Live |
| Opportunity matching | `/opportunities/recommended` | Live; API returns one best recommendation |
| Opportunity compatibility | `/opportunities/{id}/compatibility` | Live |
| Apply | `/opportunities/{id}/apply` | Live |
| Application history | — | Not exposed; UI does not fabricate it |
| Career mapping | — | Derived from profile + analysis + gaps |
| Learning recommendations | — | Derived from skill gaps |
| Rich digital portfolio | — | Profile + skills + projects + resume only |

## Backend considerations for the team

1. `POST /auth/register` currently creates a `User`; the supplied student endpoints require a corresponding `Student` row. Ensure registration/seed logic creates the student profile before testing the complete student flow.
2. The backend currently has no CORS middleware in `main.py`. The deployed backend must allow the frontend origin for browser API requests.
3. The API has no skills catalog endpoint. Therefore the frontend can display existing skills but should not invent skill IDs for new skills. Add a skills catalog endpoint if the UI needs a skill picker.
4. The API has no application-history GET endpoint. Add one later if the original full tracking table is required as live data.
