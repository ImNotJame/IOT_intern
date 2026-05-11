from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.user_auth_schema import UserResponse, LoginRequest, RegisterRequest, RefreshTokenRequest, LogoutRequest
from services.auth_service import register_service, login_service, logout_service, refresh_token_service
from util.dependencies import get_current_user, get_current_user_optional

router = APIRouter()




@router.post("/register")
async def register(data : RegisterRequest, session: AsyncSession = Depends(get_db)):
    return await register_service(data, session)


@router.post("/login", response_model=UserResponse)
async def login(data:LoginRequest, session: AsyncSession = Depends(get_db)):
    return await login_service(data, session)

@router.post("/refresh", response_model=UserResponse)
async def refresh_token(data: RefreshTokenRequest, session: AsyncSession = Depends(get_db)):
    return await refresh_token_service(data, session)


@router.post("/logout")
async def logout(
        data : LogoutRequest = None,
        current_user: dict = Depends(get_current_user_optional),
        session: AsyncSession = Depends(get_db)):
    return await logout_service(current_user,data, session)


