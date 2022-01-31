from typing import TypeVar, Generic, Callable

from common_foundation.domain.observer.basic_observer import BasicObserver

from common_foundation.domain.observer.i_observer_subject import IObserverSubject
from common_foundation.domain.observer.i_observer import IObserver

T = TypeVar('T')


class BasicObserverSubject(Generic[T], IObserverSubject[T]):
    def __init__(self, observer_factory: Callable[[Callable[[T], any]], IObserver[T]] = None):
        self._observers: list[IObserver[T]] = []
        self.observer_factory = observer_factory if observer_factory else BasicObserver

    def attach(self, observer: IObserver[T]):
        self._observers.append(observer)

    def attach_fce(self, fce: Callable[[T], any]) -> IObserver[T]:
        observer = self.observer_factory(fce)
        self._observers.append(observer)
        return observer

    def detach(self, observer: IObserver[T]):
        self._observers.remove(observer)

    def notify(self, value: T):
        for observer in self._observers:
            observer.update(value)
