from asyncio import Queue

from connect4_server.game.schemas import StreamUpdate


class Broadcaster:
    _subscribers: set[Queue[tuple[str, StreamUpdate]]]

    def __init__(self):
        self._subscribers = set()

    def subscribe(self) -> Queue[tuple[str, StreamUpdate]]:
        q: Queue[tuple[str, StreamUpdate]] = Queue()
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: Queue):
        self._subscribers.discard(q)

    async def publish(self, event: str, update: StreamUpdate):
        for q in self._subscribers:
            await q.put((event, update))
