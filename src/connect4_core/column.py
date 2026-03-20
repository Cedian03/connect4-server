from enum import StrEnum


class Column(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

    def column_index(self) -> int:
        return "ABCDEFG".index(self)
