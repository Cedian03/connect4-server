import os

from datetime import timedelta, datetime, timezone

import jwt

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Depends

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-fallback")
ALGORITHM = "HS256"
TOKEN_EXPIRY = timedelta(minutes=60)

bearer_scheme = HTTPBearer()


def create_token(user_id: int, user_name: str) -> str:
    payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": datetime.now(timezone.utc) + TOKEN_EXPIRY,
    }
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    return decode_token(credentials.credentials)
