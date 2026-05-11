from datetime import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True




class UserResponse(BaseModel):
    jwt_token: str
    refresh_token: str
    expires_at : datetime

    class Config:
        from_attributes = True


class LogoutRequest(BaseModel):
    refresh_token: str | None = None

    class Config:
        from_attributes = True