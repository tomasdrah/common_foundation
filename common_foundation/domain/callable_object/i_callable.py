import abc
from typing import TypeVar, Generic

TI = TypeVar('TI')
TO = TypeVar('TO')


class ICallable(Generic[TI, TO], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def call(self, data: TI) -> TO:
        pass

    @abc.abstractmethod
    def __call__(self, data: TI, *args, **kwargs) -> TO:
        pass
