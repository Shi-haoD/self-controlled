from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {
        "access_token": "dev-token",
        "token_type": "bearer"
    }

@router.get("/ping")
def ping():
    return {"msg": "pong"}
