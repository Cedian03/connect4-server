from typing import Any
from connect4_server.database import User, get_db_connection, Game
from fastapi import APIRouter, Depends, Query

import connect4_server.auth.dependencies as auth_deps

import connect4_server.game.schemas as game_schs


import connect4_server.user.schemas as user_schs
import connect4_server.user.services as user_svcs
import connect4_server.user.dependencies as user_deps


router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/me",
    response_model=user_schs.UserResponse,
)
async def get_me(
    user_id: int = Depends(auth_deps.get_current_user_id),
    user: User = Depends(user_deps.get_user),
):
    return dict(user)


@router.get("/search", response_model=list[user_schs.UserSearchResult])
async def search_users(
    query: str = Query(min_length=1),
):
    with get_db_connection() as conn:
        return user_svcs.search_users(query, conn)


@router.get("/{user_id}/games", response_model=list[game_schs.GameResponse])
def get_user_games(user_id: int):
    with get_db_connection() as conn:
        games: list[Game] = conn.execute(
            "SELECT * FROM games WHERE as_x = ? OR as_o = ?",
            (user_id, user_id),
        ).fetchall()
    return [dict(game) for game in games]


@router.get("/{user_id}", response_model=user_schs.UserResponse)
async def get_user(
    user: user_schs.UserResponse = Depends(user_deps.get_user),
):
    return dict(user)
