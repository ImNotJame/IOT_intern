import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from database.database import get_db
from repositories.user_session_repo import UserSessionRepository
from util.token_util import verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db)):
    try:
        payload = verify_jwt_token(token)
        user_session_repo = UserSessionRepository(session)
        user_session = await user_session_repo.get_active_user_session_by_user_id(payload.get("id"))
        if not user_session or user_session.user_jwt_token != token or not user_session.user_flag:
            raise HTTPException(status_code=401,
                                detail="Session has expired",
                                headers={"WWW-Authenticate": "Bearer"})
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail="Token has expired",
                            headers={"WWW-Authenticate": "Bearer"})
    except HTTPException:
        raise
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,
                            detail="Invalid token",
                            headers={"WWW-Authenticate": "Bearer"})


async def get_current_user_optional(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db)):
    try:
        payload = verify_jwt_token(token)
        return payload
    except(jwt.ExpiredSignatureError,jwt.InvalidTokenError):
        return None
    except HTTPException:
        return None
