import types

from rxbp.acknowledgement.continueack import continue_ack
from rxbp.acknowledgement.ack import Ack
from rxbp.acknowledgement.stopack import stop_ack
from rxbp.flowable import Flowable
from rxbp.observer import Observer
from rxbp.scheduler import Scheduler
from rxbp.typing import ElementType


class FlowableCache:
    def __init__(
            self,
            source: Flowable,
            scheduler: Scheduler = None,
    ):
        self._cache = []
        self._exception = None

        outer_self = self

        class ToCacheObserver(Observer):
            def on_next(self, elem: ElementType) -> Ack:
                try:
                    for value in elem:
                        outer_self._cache.append(value)
                except Exception as exc:
                    outer_self._exception = exc
                    return stop_ack

                return continue_ack

            def on_error(self, exc: Exception):
                outer_self._exception = exc

            def on_completed(self):
                pass

        self._observer = ToCacheObserver()

        source.subscribe(
            observer=self._observer,
            scheduler=scheduler,
            subscribe_scheduler=scheduler,
        )

    def to_list(self):
        def on_next(self, elem):
            return stop_ack

        self._observer.on_next = types.MethodType(on_next, self._observer)

        if self._exception is not None:
            raise self._exception

        return self._cache