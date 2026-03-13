from connect4_core.util import parse_moves
from typing import Optional, Self

from connect4_core.disk import Disk


WIDTH = 7
HEIGHT = 6

Matrix = list[list[Optional[Disk]]]


class Board:
    _matrix: Matrix
    _turn: int = 0

    def __init__(self):
        self._matrix = [[None for _ in range(HEIGHT)] for _ in range(WIDTH)]

    @classmethod
    def from_str(cls, s: str) -> Self:
        board = cls()
        board.play_sequence(s)
        return board

    def __getitem__(self, index: tuple[int, int]) -> Optional[Disk]:
        return self._matrix[index[0]][index[1]]

    def __setitem__(self, index: tuple[int, int], item: Optional[Disk]):
        self._matrix[index[0]][index[1]] = item

    @property
    def matrix(self) -> Matrix:
        return self._matrix

    @property
    def turn(self) -> int:
        return self._turn

    def play(self, col: int):
        if (row := self.free_row_in(col)) is None:
            raise Exception("TODO")

        self[(col, row)] = self.disk_to_play()
        self._turn += 1

    def play_sequence(self, sequence: str):
        for col in parse_moves(sequence):
            self.play(col)

    def disk_to_play(self) -> Disk:
        return Disk.X if self._turn % 2 == 0 else Disk.O

    def free_row_in(self, col: int) -> Optional[int]:
        for r, d in enumerate(self._matrix[col]):
            if d is None:
                return r

    def check_four_connected(self) -> Optional[Disk]:
        return check_four_connected(self.matrix)


def check_four_connected(matrix: Matrix) -> Optional[Disk]:
    for col in range(WIDTH):
        for row in range(HEIGHT):
            disk = matrix[col][row]
            if disk is None:
                continue

            if col <= WIDTH - 4 and all(matrix[col + i][row] == disk for i in range(4)):
                return disk
            if row <= HEIGHT - 4 and all(
                matrix[col][row + i] == disk for i in range(4)
            ):
                return disk
            if (
                col <= WIDTH - 4
                and row >= 3
                and all(matrix[col + i][row - i] == disk for i in range(4))
            ):
                return disk
            if (
                col <= WIDTH - 4
                and row <= HEIGHT - 4
                and all(matrix[col + i][row + i] == disk for i in range(4))
            ):
                return disk

    return None
