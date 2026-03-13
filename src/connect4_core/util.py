from typing import Iterator


def parse_moves(s: str) -> Iterator[int]:
    for chr in s:
        yield char_to_column(chr)


def char_to_column(chr: str) -> int:
    return "ABCDEFG".index(chr)


def column_to_char(col: int) -> str:
    return "ABCDEFG"[col]
