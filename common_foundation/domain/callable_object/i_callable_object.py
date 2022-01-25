import abc
from typing import TypeVar, Generic, Callable

from common_foundation.domain.callable_object.i_callable import ICallable

TI = TypeVar('TI')
TO = TypeVar('TO')


class ICallableObject(Generic[TI, TO], ICallable[TI, TO]):

    @staticmethod
    @abc.abstractmethod
    def create_from_fce(fce: Callable[[TI], TO]) -> "ICallableObject[TI,TO]":
        pass

    @staticmethod
    @abc.abstractmethod
    def change_fce(self, fce: Callable[[TI], TO]):
        pass
