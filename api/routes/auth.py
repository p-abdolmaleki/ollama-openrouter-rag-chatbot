from fastapi import APIRouter, HTTPException
from ..schemas.auth import LoginRequest, LoginResponse


router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    if not data.username:
        raise HTTPException(status_code=400, detail="Username required")
    return {"user_id": data.username}

@router.post("/logout")
def logout():
    return {"message": "Logged out"}