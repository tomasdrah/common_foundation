from common_foundation.domain.event_recorder import BasicEventRecorder
from common_foundation.domain.events import IEvent


class DummyMyEvent(IEvent):
    pass


def test_basic_event_recorder():
    recorder = BasicEventRecorder()
    event = DummyMyEvent()
    recorder.record_event(event)
    assert recorder.events
    assert recorder.events[0] == event
    recorder.clear_events()
    assert len(recorder.events) == 0
