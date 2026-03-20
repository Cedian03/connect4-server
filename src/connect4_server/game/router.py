from connect4_server.database import get_db_connection
import asyncio
from collections.abc import AsyncIterable

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import EventSourceResponse
from fastapi.sse import ServerSentEvent

from connect4_server.auth.dependencies import get_current_user_id
from connect4_server.connect4 import Game, Column

from connect4_server.game import schemas as game_schs
from connect4_server.game import services as game_svcs
from connect4_server.game import exceptions as game_excs
from connect4_server.game import dependencies as game_deps

from connect4_server.game.utils import Broadcaster

router = APIRouter(prefix="/game", tags=["game"])

broadcasters: dict[int, Broadcaster] = {}


def get_broadcaster(game_id: int) -> Broadcaster:
    if game_id not in broadcasters:
        broadcasters[game_id] = Broadcaster()
    return broadcasters[game_id]


@router.post(
    "",
    response_model=game_schs.GameCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_game(
    data: game_schs.GameCreate,
):
    with get_db_connection() as conn:
        game_id = game_svcs.create_game(data, conn)
    return {"id": game_id}


@router.get(
    "/{game_id}",
    response_model=game_schs.GameResponse,
)
async def get_game(
    game: Game = Depends(game_deps.get_game),
):
    return vars(game)


@router.post(
    "/{game_id}/play",
    response_model=game_schs.GameResponse,
)
async def play(
    game_id: int,
    column: Column,
    game: Game = Depends(game_deps.get_game),
    user_id: int = Depends(get_current_user_id),
):
    if game.has_concluded or game.user_to_play() != user_id:
        raise game_excs.NotYourTurn()

    game = game_svcs.play(game, column)
    await get_broadcaster(game_id).publish(
        "game-update",
        game_schs.StreamUpdate(**vars(game)),
    )

    return vars(game)


@router.post(
    "/{game_id}/forfeit",
    response_model=game_schs.GameResponse,
)
async def forfeit(
    game_id: int,
    game: Game = Depends(game_deps.get_game),
    user_id: int = Depends(get_current_user_id),
):
    if game.has_concluded:
        raise game_excs.GameConcluded()

    game = game_svcs.forfeit(game, user_id)
    await get_broadcaster(game_id).publish(
        "game-update",
        game_schs.StreamUpdate(**vars(game)),
    )

    return vars(game)


@router.get(
    "/{game_id}/stream",
    response_class=EventSourceResponse,
)
async def stream(
    game_id: int,
    request: Request,
) -> AsyncIterable[ServerSentEvent]:
    queue = get_broadcaster(game_id).subscribe()

    try:
        while True:
            if await request.is_disconnected():
                break

            try:
                event, data = await asyncio.wait_for(queue.get(), timeout=15)
                yield ServerSentEvent(event=event, data=data)
            except asyncio.TimeoutError:
                yield ServerSentEvent(comment="keepalive")
    finally:
        get_broadcaster(game_id).unsubscribe(queue)
