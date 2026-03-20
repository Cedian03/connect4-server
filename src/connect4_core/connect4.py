from connect4_core.exceptions import InvalidMoveError
from connect4_core.column import Column
from connect4_core import Board, Disk


class Connect4:
    _board: Board
    _has_concluded: bool = False
    _winner: Disk | None = None

    def __init__(self):
        self._board = Board()

    @property
    def has_concluded(self) -> bool:
        return self._has_concluded

    def drop(self, column: Column) -> int:
        if (row := self._board.free_row_in(column.column_index())) is None:
            raise InvalidMoveError()

        return row
