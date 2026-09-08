from fastapi import FastAPI

from app.routers import auth, users


app = FastAPI(
    title="SIH Academia-Industry Collaboration API",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": "SIH Backend is running!"
    }