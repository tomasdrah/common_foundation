import logging
from typing import Callable

from common_foundation.domain.callable_object import ICallableObject

TI = Exception
TO = None


class BasicExceptionLogger(ICallableObject[TI, TO]):
    def __init__(self, name="Default"):
        self.logger = logging.getLogger(name)

    def call(self, data: Exception):
        self.logger.exception(data)

    def __call__(self, data: TI, *args, **kwargs) -> TO:
        self.call(data)

    @staticmethod
    def create_from_fce(fce: Callable[[TI], TO]) -> "ICallableObject[TI,TO]":
        return BasicExceptionLogger()

    @staticmethod
    def change_fce(self, fce: Callable[[TI], TO]):
        pass
