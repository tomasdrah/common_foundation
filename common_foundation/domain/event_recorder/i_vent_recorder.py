import abc

from common_foundation.domain.events import IEvent


class IEventRecorder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def record_event(self, event: IEvent) -> None:
        pass

    @property
    @abc.abstractmethod
    def events(self) -> list[IEvent]:
        pass

    @abc.abstractmethod
    def clear_events(self) -> None:
        pass
