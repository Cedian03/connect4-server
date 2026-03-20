from connect4_server.game.schemas import StreamUpdate
from enum import StrEnum
from dataclasses import dataclass, field
from typing import Optional

from connect4_core import Disk
from connect4_core import Board


class Column(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

    def as_index(self) -> int:
        return "ABCDEFG".index(self)


@dataclass
class Game:
    id: int
    as_x: int
    as_o: int
    moves: str = ""
    winner: Optional[Disk] = None
    forfeit: Optional[bool] = None
    board: Board = field(init=False)

    def __post_init__(self):
        self.board = Board.from_str(self.moves)

    @property
    def has_concluded(self) -> bool:
        return self.forfeit is not None

    def disk_of_user(self, user_id: int) -> Optional[Disk]:
        if user_id == self.as_x:
            return Disk.X
        elif user_id == self.as_o:
            return Disk.O

    def user_of_disk(self, disk: Disk) -> int:
        match disk:
            case Disk.X:
                return self.as_x
            case Disk.O:
                return self.as_o

    def user_to_play(self) -> int:
        return self.user_of_disk(self.board.disk_to_play())

    def as_update(self) -> StreamUpdate:
        return StreamUpdate(
            moves=self.moves,
            winner=self.winner,
            forfeit=self.forfeit,
        )
