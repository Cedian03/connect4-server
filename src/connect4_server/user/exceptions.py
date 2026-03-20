from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, game_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {game_id} not found",
        )
