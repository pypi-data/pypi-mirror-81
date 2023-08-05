import asyncio
import datetime
import time
from threading import Thread

from rx.core.typing import ScheduledAction, RelativeTime, AbsoluteTime
from rx.disposable import Disposable

from rxbp.scheduler import SchedulerBase


class AsyncIOScheduler(SchedulerBase, Disposable):
    def __init__(self, loop: asyncio.AbstractEventLoop = None, new_thread: bool = None):
        super().__init__()

        self.loop: asyncio.AbstractEventLoop = loop or asyncio.new_event_loop()

        if new_thread is None or new_thread is True:
            t = Thread(target=self.start_loop)
            t.setDaemon(True)
            t.start()

    @property
    def idle(self) -> bool:
        return True

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    @property
    def is_order_guaranteed(self) -> bool:
        return True

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    @property
    def now(self):
        # return self.loop.time()
        return datetime.datetime.now()

    def schedule(self,
                 action: ScheduledAction,
                 state=None):
        def func():
            action(self, state)

        handle = self.loop.call_soon_threadsafe(func)

        def dispose():
            handle.cancel()

        return Disposable(dispose)

    def schedule_relative(self,
                          duetime: RelativeTime,
                          action: ScheduledAction,
                          state=None):

        if isinstance(duetime, datetime.datetime):
            timedelta = duetime - datetime.datetime.fromtimestamp(0)
            timespan = float(timedelta.total_seconds())
        elif isinstance(duetime, datetime.timedelta):
            timespan = float(duetime.total_seconds())
        else:
            timespan = duetime

        def _():
            def func():
                action(self, state)

            self.loop.call_later(timespan, func)

        handle = self.loop.call_soon_threadsafe(_)

        def dispose():
            handle.cancel()

        return Disposable(dispose)

    def schedule_absolute(self,
                          duetime: AbsoluteTime,
                          func: ScheduledAction,
                          state=None):
        if isinstance(duetime, datetime.datetime):
            timedelta = (duetime - datetime.datetime.now()).total_seconds()
        else:
            timedelta = duetime

        return self.schedule_relative(timedelta, func)

    def dispose(self):
        def _():
            self.loop.stop()

        self.loop.call_soon_threadsafe(_)
