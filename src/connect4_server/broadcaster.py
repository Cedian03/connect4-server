from asyncio import Queue
from typing import Optional

from pydantic import BaseModel

from connect4_core import Disk


class Update(BaseModel):
    moves: str
    winner: Optional[Disk]
    forfeit: Optional[bool]


class Broadcaster:
    _subscribers: set[Queue[tuple[str, Update]]]

    def __init__(self):
        self._subscribers = set()

    def subscribe(self) -> Queue[tuple[str, Update]]:
        q: Queue[tuple[str, Update]] = Queue()
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: Queue):
        self._subscribers.discard(q)

    async def publish(self, event: str, update: Update):
        for q in self._subscribers:
            await q.put((event, update))
