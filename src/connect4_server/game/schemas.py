from typing import Optional

from pydantic import BaseModel, ConfigDict

from connect4_core import Disk


class GameCreate(BaseModel):
    as_x: int
    as_o: int


class GameCreateResponse(BaseModel):
    id: int


class GameResponse(BaseModel):
    id: int
    as_x: int
    as_o: int
    moves: str
    winner: Optional[Disk] = None
    forfeit: Optional[bool] = None


class StreamUpdate(BaseModel):
    moves: str
    winner: Optional[Disk]
    forfeit: Optional[bool]
