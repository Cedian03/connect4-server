from fastapi import HTTPException, status


class GameNotFound(HTTPException):
    def __init__(self, game_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {game_id} not found",
        )


class NotYourTurn(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not your turn",
        )


class GameConcluded(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game has already concluded",
        )


class InvalidMove(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid move",
        )


class NotYourGame(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a player in this game",
        )
