from connect4_server.database import User
import bcrypt

from sqlite3 import Connection

import connect4_server.auth.exceptions as auth_excs
from .exceptions import InvalidCredentials
from .utils import create_token


def register(username: str, password: str, conn: Connection) -> int | None:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    conn.commit()

    return cursor.lastrowid


def authenticate(username: str, password: str, conn: Connection) -> str | None:
    user: User | None = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    ).fetchone()

    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"]):
        return None

    return create_token(user["id"], user["username"])
