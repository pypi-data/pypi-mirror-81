from dataclasses import dataclass
from typing import Callable, Any

from rxbp.mixins.flowablemixin import FlowableMixin
from rxbp.observables.doactionobservable import DoActionObservable
from rxbp.subscriber import Subscriber


@dataclass
class DoActionFlowable(FlowableMixin):
    source: FlowableMixin
    on_next: Callable[[Any], None] = None
    on_completed: Callable[[], None] = None
    on_error: Callable[[Exception], None] = None
    on_disposed: Callable[[], None] = None

    def unsafe_subscribe(self, subscriber: Subscriber):
        subscription = self.source.unsafe_subscribe(subscriber=subscriber)

        return subscription.copy(
            observable=DoActionObservable(
                source=subscription.observable,
                on_next=self.on_next,
                on_completed=self.on_completed,
                on_error=self.on_error,
                on_disposed=self.on_disposed,
            ),
        )
