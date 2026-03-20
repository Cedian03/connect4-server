from sqlite3 import Connection
from connect4_server.database import get_db_connection, User

from connect4_server.user import schemas as user_schs


def get_user(user_id: int, conn: Connection) -> User | None:
    row = conn.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    if row is None:
        return None

    return User(**dict(row))


def search_users(query: str, conn: Connection) -> list[User]:
    users = conn.execute(
        "SELECT id, username FROM users WHERE username LIKE ?", (f"{query}%",)
    ).fetchall()
    return [User(**dict(user)) for user in users]
