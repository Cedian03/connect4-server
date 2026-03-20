from connect4_server.database import get_db_connection
from connect4_server.connect4 import Game


import connect4_server.game.services as game_svcs
import connect4_server.game.exceptions as game_excs


async def get_game(
    game_id: int,
) -> Game:
    with get_db_connection() as conn:
        game = game_svcs.get_game(game_id, conn)

    if not game:
        raise game_excs.GameNotFound(game_id)

    return game
