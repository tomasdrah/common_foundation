import abc
from typing import Generic, TypeVar

from common_foundation.domain.use_case_base.response_object import ResponseObject

TO = TypeVar('TO')


class IPresenter(Generic[TO], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def present(self, output_dto: ResponseObject[TO]):
        pass
