import abc
import logging
from typing import TypeVar, Generic

from common_foundation.domain.event_recorder import IEventRecorder
from common_foundation.domain.events.i_event import IEvent
from common_foundation.domain.callable_object import ICallable
from common_foundation.domain.use_case_base.exception_logger import BasicExceptionLogger
from common_foundation.domain.use_case_base.i_presenter import IPresenter
from common_foundation.domain.use_case_base.i_execute import IExecute
from common_foundation.domain.use_case_base.response_object import ResponseObject

# generic
TI = TypeVar('TI')
TO = TypeVar('TO')


class UseCaseBase(Generic[TI, TO], IExecute[TI, TO]):
    def __init__(self):
        self.exception_handlers: list[ICallable[Exception, any]] = [BasicExceptionLogger()]
        self.event_recorders: list[IEventRecorder] = []
        self._output_boundaries: list[IPresenter[TO]] = []
        self.logger = logging.getLogger(__name__)

    @property
    def output_boundaries(self) -> list[IPresenter[TO]]:
        return self._output_boundaries

    def execute(self, request_object: TI) -> ResponseObject[TO]:
        try:
            input_object = self._create_input(request_object)
            return self.process_request(input_object)
        except Exception as exc:
            self.handle_exception(exc)
            return self.create_response(success=False)

    def _create_input(self, request_object: TI):
        try:
            if not isinstance(request_object, tuple):
                request_object = (request_object,)
            result = self.create_input(request_object)
            return result
        except Exception as exc:
            raise Exception(f"Error: Bad request object, object: {request_object}, exc_msg: {exc}")

    @abc.abstractmethod
    def process_request(self, request_object) -> ResponseObject[TO]:
        raise NotImplementedError(
            "process_request() not implemented by UseCaseBase class")

    def present_output_boundary(self, msg: TO = None, success=True):
        response = self.create_response(msg, success)
        try:
            for boundary in self.output_boundaries:
                boundary.present(response)
        except Exception as exc:
            self.handle_exception(exc)

    def handle_exception(self, exc: Exception):
        for handler in self.exception_handlers:
            try:
                handler.call(exc)
            except Exception as exc:
                self.logger.error(f"Error: Something went wrong with exception_handler: {handler}, exc_msg: {exc}")

    def record_event(self, event: IEvent):
        for recorder in self.event_recorders:
            recorder.record_event(event)

    def create_response(self, msg: TO = None, success=True) -> ResponseObject[TO]:
        return ResponseObject(success=success, msg=msg)

    @staticmethod
    @abc.abstractmethod
    def create_input(value: TI) -> any:
        pass
