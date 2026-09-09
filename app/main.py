from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    users,
    assessment,
    skill_analysis,
    skill_gap,
    opportunities,
    seed
)

app = FastAPI(
    title="SIH Academia-Industry Collaboration API",
    version="1.0.0"
)

# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# ROUTERS
# --------------------------------------------------

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(assessment.router)
app.include_router(skill_analysis.router)
app.include_router(skill_gap.router)
app.include_router(opportunities.router)
app.include_router(seed.router)


@app.get("/")
def root():
    return {
        "message": "SIH Backend is running!"
    }