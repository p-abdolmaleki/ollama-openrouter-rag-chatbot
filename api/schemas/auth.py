from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str

class LoginResponse(BaseModel):
    user_id: str