from fastapi import APIRouter

from connect4_server.database import get_db_connection

import connect4_server.auth.schemas as auth_schs
import connect4_server.auth.services as auth_svcs
import connect4_server.auth.exceptions as auth_excs


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=auth_schs.TokenResponse,
)
async def register(
    req: auth_schs.AuthRequest,
):
    with get_db_connection() as conn:
        user_id = auth_svcs.register(req.username, req.password, conn)

    if user_id is None:
        raise auth_excs.InvalidCredentials()


@router.post(
    "/authenticate",
    response_model=auth_schs.TokenResponse,
)
async def authenticate(
    req: auth_schs.AuthRequest,
):
    with get_db_connection() as conn:
        token = auth_svcs.authenticate(
            req.username,
            req.password,
            conn,
        )

    if token is None:
        raise auth_excs.InvalidCredentials()

    return {"token": token}
