from fastapi import APIRouter, HTTPException
from ..schemas.auth import LoginRequest, LoginResponse
from ..schemas.common import ApiResponse

router = APIRouter()

@router.post("/login", response_model=ApiResponse)
def login(data: LoginRequest):
    if not data.username:
        raise HTTPException(status_code=400, detail="Username required")
    return ApiResponse(data={"user_id": data.username})

@router.post("/logout", response_model=ApiResponse)
def logout():
    return ApiResponse(message="Logged out")