from datetime import timedelta, datetime

import jwt
import pytz
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import UserRepository
from repositories.user_session_repo import UserSessionRepository
from schemas.user_auth_schema import LoginRequest, UserResponse, RegisterRequest, RefreshTokenRequest, LogoutRequest
from util.password_util import hash_password, verify_password
from util.token_util import create_jwt_token, verify_refresh_token



async def register_service(data: RegisterRequest, session: AsyncSession):
    user_repo = UserRepository(session)
    username = data.username
    password = data.password
    user = await user_repo.get_user_by_username(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    await user_repo.create_user(username, hashed_password)
    return {"user": data}


async def login_service(
        user_auth: LoginRequest,
        session: AsyncSession):

    try:

        current_date = datetime.now(tz=pytz.timezone('Asia/Bangkok'))


        user_repo = UserRepository(session)
        user = await user_repo.get_user_by_username(user_auth.username)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid username or password")

        validate_password = verify_password(user_auth.password, user.hashed_password)
        if not validate_password:
            raise HTTPException(status_code=400, detail="Invalid username or password")

        expires = current_date + timedelta(minutes=60)

        data = {
            "id": user.id,
            "username": user.username,
        }

        jwt_token = create_jwt_token(data, expire_in=1)
        refresh_token = create_jwt_token(data, expire_in=60)

        res = UserResponse(
            jwt_token=jwt_token,
            refresh_token=refresh_token,
            expires_at=expires
        )


        user_session_repo = UserSessionRepository(session)
        await user_session_repo.create_user_session(user.id, jwt_token, refresh_token)

        return res


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def logout_service(current_user: dict,data:LogoutRequest, session: AsyncSession):
    user_id = current_user.get("id") if current_user else None

    if not user_id and data and data.refresh_token:
        try:
            payload = verify_refresh_token(data.refresh_token)
            user_id = payload.get("id")
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise HTTPException(status_code=401, detail="Invalid session")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user session")

    user_session_repo = UserSessionRepository(session)
    await user_session_repo.update_user_session_by_dict(user_id, {"user_flag": False,
                                                                  "user_logout_time": datetime.now(tz=pytz.timezone('Asia/Bangkok'))})
    return {"message": "Logged out successfully"}


async def refresh_token_service(data: RefreshTokenRequest, session: AsyncSession):
    try:
        payload = verify_refresh_token(data.refresh_token)
        user_id = payload.get("id")
        username = payload.get("username")

        if not user_id or not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_session_repo = UserSessionRepository(session)
        existing_session = await user_session_repo.get_active_user_session_by_user_id(user_id)
        if not existing_session or existing_session.user_refresh_token != data.refresh_token:
            raise HTTPException(status_code=401, detail="Session has expired")

        token_data = {
            "id": user_id,
            "username": username,
        }
        jwt_token = create_jwt_token(token_data, expire_in=1)


        existing_session.user_jwt_token = jwt_token
        await session.commit()

        return UserResponse(
            jwt_token=jwt_token,
            refresh_token=data.refresh_token,
            expires_at=datetime.now(tz=pytz.timezone('Asia/Bangkok')) + timedelta(minutes=60)
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except HTTPException:
        raise



