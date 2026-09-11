from __future__ import annotations
import asyncio
from dataclasses import dataclass

@dataclass(frozen=True)
class Tick:
    symbol: str
    price: float
    volume: int
    sequence: int

class AsyncTickPipeline:
    """Bounded async queue demonstrates back-pressure and graceful shutdown."""
    def __init__(self, max_queue=1000):
        self.queue = asyncio.Queue(maxsize=max_queue)
        self.stop_event = asyncio.Event()

    async def publish(self, tick: Tick):
        await self.queue.put(tick)  # producer naturally blocks when queue is full

    async def consume(self, handler):
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                tick = await asyncio.wait_for(self.queue.get(), timeout=0.1)
            except asyncio.TimeoutError:
                continue
            try:
                await handler(tick)
            finally:
                self.queue.task_done()

    async def shutdown(self):
        self.stop_event.set()
        await self.queue.join()
