from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.models import User

app = FastAPI(title="BookFlow AI")

app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def health():
    return {"status": "ok", "app": "BookFlow AI"}

