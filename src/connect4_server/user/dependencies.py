from connect4_server.database import get_db_connection, User

from connect4_server.user import services as game_svcs
from connect4_server.user import exceptions as user_excs


def get_user(user_id: int) -> User:
    with get_db_connection() as conn:
        user = game_svcs.get_user(user_id, conn)

    if user is None:
        raise user_excs.UserNotFound(user_id)

    return user
