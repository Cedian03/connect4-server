from __future__ import annotations

from enum import StrEnum


class Disk(StrEnum):
    X = "X"
    O = "O"

    def __invert__(self) -> Disk:
        match self:
            case Disk.X:
                return Disk.O
            case Disk.O:
                return Disk.X
