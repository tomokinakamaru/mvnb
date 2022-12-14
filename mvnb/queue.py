from asyncio import Queue as Queue_
from asyncio import create_task


class Queue(object):
    def __init__(self, func):
        self._queue = Queue_()
        self._func = func
        self._task = None

    def start(self):
        self._task = create_task(self._watch())
        return self._task

    def stop(self):
        self._task.cancel()
        self._task = None

    async def put(self, msg, *args):
        await self._queue.put((msg, args))

    async def _watch(self):
        while True:
            msg, args = await self._queue.get()
            await self._func(msg, *args)
