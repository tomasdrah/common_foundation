import abc
from typing import TypeVar, Generic, Callable

from common_foundation.domain.observer.i_observer import IObserver

T = TypeVar('T')


class IObserverSubject(Generic[T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def attach(self, observer: IObserver[T]):
        raise NotImplementedError

    @abc.abstractmethod
    def attach_fce(self, fce: Callable[[T], any]) -> IObserver[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def detach(self, observer: IObserver[T]):
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self, value: T):
        raise NotImplementedError
