# AIC Portal — SIH Frontend

Backend-synced student frontend built from the supplied AIC Portal reference screens and the supplied FastAPI backend.

## Run

1. Install Node.js.
2. Copy `.env.example` to `.env`.
3. Set `VITE_API_BASE_URL` to the team's deployed backend URL.
4. Run `npm install`.
5. Run `npm run dev` for development or `npm run build` for production.

The frontend does **not** require the backend to run on the same machine. Only the deployed API URL is required.

## Live endpoints used

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/verify-email?token=...`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `GET /users/me`
- `GET/PUT /users/me/profile`
- `GET /users/me/skills`
- `POST/DELETE /users/me/skills`
- `GET /users/me/projects`
- `POST/DELETE /users/me/projects`
- `GET /assessment/current`
- `POST /assessment/submit`
- `GET /assessment/result`
- `GET /skills/analysis`
- `GET /skills/gaps`
- `GET /opportunities/recommended`
- `GET /opportunities/{id}/compatibility`
- `POST /opportunities/{id}/apply`

## Intentional backend-aligned changes

- Opportunity Matching shows the single ranked recommendation exposed by the API; it does not invent a multi-opportunity feed or unsupported filters.
- Application Tracking shows the live application count from the profile endpoint, but does not fabricate application history because no GET application-history endpoint exists.
- Career Mapping is derived from profile + skill analysis + skill gaps because no dedicated career mapping endpoint exists.
- Learning Recommendations are derived from live skill gaps because no course/catalog recommendation endpoint exists.
- Digital Portfolio only treats profile/skills/projects/resume data as live because richer portfolio entities are not exposed by the supplied API.
- Skill/project creation respects the backend's query-parameter based POST signatures.
- Authenticated requests automatically use `Authorization: Bearer <access_token>`.
