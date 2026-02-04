from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI(
    title="Self Controlled Backend",
    version="0.1.0"
)

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
