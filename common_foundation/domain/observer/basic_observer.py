from typing import TypeVar, Generic, Callable

from common_foundation.domain.observer import IObserver

T = TypeVar('T')


class BasicObserver(Generic[T], IObserver[T]):
    def __init__(self, fce: Callable[[T], any]):
        self._fce = fce

    def update(self, value: T):
        return self._fce(value)
