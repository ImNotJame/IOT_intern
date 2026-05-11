from datetime import datetime, timedelta

import jwt
import pytz
from dotenv import load_dotenv
import os

from schemas.user_auth_schema import UserResponse

ALGORITHM = "HS256"

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


bangkok_tz = pytz.timezone('Asia/Bangkok')


def create_jwt_token(data: dict, expire_in: int = 15)-> str:
    expire = datetime.now(bangkok_tz) + timedelta(minutes=expire_in)
    payload = data.copy()
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt(token: str)-> str:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return "valid"
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"



def verify_jwt_token(token: str)-> dict:


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


def verify_refresh_token(token: str)-> dict:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid refresh token")



def create_user_response(user) -> UserResponse:


    data ={
        "id": user.id,
        "username": user.username,
    }

    jwt_token = create_jwt_token(data, expire_in=3)
    refresh_token = create_jwt_token(data, expire_in=15)

    return UserResponse(
        jwt_token=jwt_token,
        refresh_token=refresh_token,
        expires_at=datetime.now(bangkok_tz) + timedelta(minutes=15)
    )