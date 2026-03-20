import jwt

from datetime import datetime, timezone

from .constants import TOKEN_EXPIRY, JWT_SECRET


def create_token(user_id: int, user_name: str) -> str:
    payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": datetime.now(timezone.utc) + TOKEN_EXPIRY,
    }
    return jwt.encode(payload, key=JWT_SECRET, algorithm="HS256")
