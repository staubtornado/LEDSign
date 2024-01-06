from asyncio import sleep


class Thread:
    def __init__(self, loop, target, *args, **kwargs) -> None:
        self.loop = loop
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self._should_run = None
        self._task = None

    def start(self) -> None:
        self._should_run = True
        self._task = self.loop.create_task(self._run())

    def cancel(self) -> None:
        self._should_run = False

    def update(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    async def _run(self) -> None:
        while self._should_run:
            await self.target(*self.args, **self.kwargs)
            await sleep(0)
