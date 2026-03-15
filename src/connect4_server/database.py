import sqlite3
import os

from typing import Iterator
from contextlib import contextmanager, asynccontextmanager

from fastapi import FastAPI


DB_PATH = os.environ.get("DB_PATH", "./app.db")


@contextmanager
def get_db_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                username        TEXT    NOT NULL    UNIQUE,
                password_hash   TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                as_x    INTEGER NOT NULL,
                as_o    INTEGER NOT NULL,
                moves   TEXT    NOT NULL,
                winner  CHAR,
                forfeit BOOLEAN
            )
        """)
    yield
