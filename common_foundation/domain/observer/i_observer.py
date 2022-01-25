import abc
from typing import TypeVar, Generic

T = TypeVar('T')


class IObserver(Generic[T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, value: T):
        raise NotImplementedError
