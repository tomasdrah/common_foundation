from common_foundation.domain.callable_object.i_callable_object import ICallableObject
from typing import TypeVar, Generic, Callable

TI = TypeVar('TI')
TO = TypeVar('TO')


class BasicCallableObject(Generic[TI, TO], ICallableObject[TI, TO]):
    def __init__(self, fce: Callable[[TI], TO] = None):
        self._fce = fce

    def call(self, data: TI) -> TO:
        return self._fce(data)

    def __call__(self, data: TI, *args, **kwargs) -> TO:
        return self.call(data)

    @staticmethod
    def create_from_fce(fce: Callable[[TI], TO]) -> "ICallableObject[TI,TO]":
        return BasicCallableObject(fce)

    def change_fce(self, fce: Callable[[TI], TO]):
        self._fce = fce
