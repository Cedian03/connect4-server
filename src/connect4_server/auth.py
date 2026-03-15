import os

from datetime import timedelta, datetime, timezone

import jwt
import bcrypt

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel

from connect4_server.database import get_db_connection


SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-fallback")
ALGORITHM = "HS256"
TOKEN_EXPIRY = timedelta(minutes=60)

router = APIRouter()
bearer_scheme = HTTPBearer()


class AuthRequest(BaseModel):
    username: str
    password: str


@router.post("/signup")
def signup(req: AuthRequest):
    password_hash = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt())

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (req.username, password_hash),
        )
        conn.commit()

    return signin(req)


@router.post("/signin")
def signin(req: AuthRequest):
    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (req.username,)
        ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="No user by that name")

    if not user or not bcrypt.checkpw(req.password.encode(), user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": create_token(user["id"], user["username"])}


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
