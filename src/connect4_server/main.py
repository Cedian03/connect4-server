import os

from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from connect4_core.disk import Disk
from connect4_core.util import column_to_char

from connect4_server.database import get_db_connection, lifespan
from connect4_server.auth import router as auth_router, get_current_user
from connect4_server.game import Game

FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

app = FastAPI(lifespan=lifespan, root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")


@app.get("/")
def root():
    return RedirectResponse("/docs")


@app.get("/user/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return get_user(current_user["sub"])


@app.get("/user/{user_id}")
def get_user(user_id: int):
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return dict(user)


@app.post("/game")
def create_game(
    as_x: int,
    as_o: int,
    moves: str = "",
    winner: Optional[Disk] = None,
    forfeit: Optional[bool] = None,
):
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO games (as_x, as_o, moves, winner, forfeit) VALUES (?, ?, ?, ?, ?)",
            (as_x, as_o, moves, winner, forfeit),
        )
        conn.commit()
        new_game = conn.execute(
            "SELECT * FROM games WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()

    return new_game


@app.get("/game/{game_id}")
def get_game(game_id: int):
    with get_db_connection() as conn:
        game = conn.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return dict(game)


@app.post("/game/{game_id}/play")
async def play_column(
    game_id: int,
    column: int,
    current_user: dict = Depends(get_current_user),
):
    with get_db_connection() as conn:
        game = conn.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        game = Game(**game)

        if game.user_to_play() != int(current_user["sub"]):
            raise HTTPException(
                status_code=400,
                detail="Not ur turn buddy",
            )

        if game.has_concluded:
            raise HTTPException(
                status_code=400,
                detail="Attempt make a play in a game that already concluded",
            )

        try:
            game.board.play(column)
        except Exception as _e:
            raise HTTPException(status_code=400, detail="Invalid move")

        game.moves += column_to_char(column)
        winner = game.board.check_four_connected()
        if winner:
            game.winner = winner
            game.forfeit = False
        elif game.board.turn == 7 * 6:
            game.forfeit = False

        conn.execute(
            "UPDATE games SET moves = ?, winner = ?, forfeit = ? WHERE id = ?",
            (game.moves, game.winner, game.forfeit, game.id),
        )
        conn.commit()

        game = conn.execute("SELECT * FROM games WHERE id = ?", (game.id,)).fetchone()
    return game


@app.post("/game/{game_id}/forfeit")
def forfeit_game(
    game_id: int,
    current_user: dict = Depends(get_current_user),
):
    with get_db_connection() as conn:
        game = conn.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        game = Game(**game)

        disk = game.disk_of_user(int(current_user["sub"]))
        if game.has_concluded or not disk:
            raise HTTPException(status_code=400, detail="Ur not in this game buddy")

        game.winner = ~disk
        game.forfeit = True
        conn.execute(
            "UPDATE games SET winner = ?, forfeit = ? WHERE id = ?",
            (game.winner, game.forfeit, game.id),
        )
        conn.commit()

        game = conn.execute("SELECT * FROM games WHERE id = ?", (game.id,)).fetchone()
    return game
