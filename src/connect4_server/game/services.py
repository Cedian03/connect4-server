from connect4_core.exceptions import InvalidMoveError
from sqlite3 import Connection
from connect4_server.database import get_db_connection
from connect4_server.connect4 import Game, Column
from connect4_server.game import schemas as game_schs
from connect4_server.game import exceptions as game_excs


def create_game(data: game_schs.GameCreate, conn: Connection) -> int:
    cursor = conn.execute(
        "INSERT INTO games (as_x, as_o, moves) VALUES (?, ?, ?)",
        (data.as_x, data.as_o, ""),
    )
    conn.commit()

    return cursor.lastrowid  # type: ignore


def get_game(game_id: int, conn: Connection) -> Game | None:
    game = conn.execute(
        "SELECT * FROM games WHERE id = ?",
        (game_id,),
    ).fetchone()

    if not game:
        return None

    return Game(**dict(game))


def play(game: Game, column: Column) -> Game:
    try:
        game.board.play(column.as_index())
    except InvalidMoveError:
        raise game_excs.InvalidMove()

    game.moves += column

    winner = game.board.check_four_connected()
    if winner:
        game.winner = winner
        game.forfeit = False
    elif game.board.turn == 7 * 6:
        game.forfeit = False

    with get_db_connection() as conn:
        conn.execute(
            "UPDATE games SET moves = ?, winner = ?, forfeit = ? WHERE id = ?",
            (game.moves, game.winner, game.forfeit, game.id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM games WHERE id = ?", (game.id,)).fetchone()
    return Game(**row)


def forfeit(game: Game, user_id: int) -> Game:
    disk = game.disk_of_user(user_id)
    if disk is None:
        raise game_excs.NotYourGame()
    game.winner = ~disk
    game.forfeit = True

    with get_db_connection() as conn:
        conn.execute(
            "UPDATE games SET winner = ?, forfeit = ? WHERE id = ?",
            (game.winner, game.forfeit, game.id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM games WHERE id = ?", (game.id,)).fetchone()
    return Game(**row)
