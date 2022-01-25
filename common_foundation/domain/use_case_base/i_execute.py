import abc
from typing import TypeVar, Generic

from common_foundation.domain.use_case_base.response_object import ResponseObject

TI = TypeVar('TI')
TO = TypeVar('TO')


class IExecute(Generic[TI, TO], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, request_object: TI) -> ResponseObject[TO]:
        pass
