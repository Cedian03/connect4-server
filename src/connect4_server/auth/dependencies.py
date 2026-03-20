from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from typing import Any
from fastapi import Depends

from connect4_server.auth.constants import JWT_SECRET

bearer_scheme = HTTPBearer()


async def parse_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, Any]:
    return jwt.decode(
        credentials.credentials.encode(), JWT_SECRET, algorithms=["HS256"]
    )


async def get_current_user_id(
    data: dict[str, Any] = Depends(parse_jwt_token),
) -> int:
    return int(data["sub"])
