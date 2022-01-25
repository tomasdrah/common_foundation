from common_foundation.domain.event_recorder.i_vent_recorder import IEventRecorder
from common_foundation.domain.events import IEvent


class BasicEventRecorder(IEventRecorder):
    def __init__(self) -> None:
        self._pending_domain_events: list[IEvent] = []

    def record_event(self, event: IEvent) -> None:
        self._pending_domain_events.append(event)

    @property
    def events(self) -> list[IEvent]:
        return self._pending_domain_events.copy()

    def clear_events(self) -> None:
        self._pending_domain_events.clear()
