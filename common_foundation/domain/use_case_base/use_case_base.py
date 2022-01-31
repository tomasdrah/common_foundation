import abc
import logging
import traceback
from typing import TypeVar, Generic, Callable

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
        self._input_factory = None
        self._output_factory = None

    @property
    def output_boundaries(self) -> list[IPresenter[TO]]:
        return self._output_boundaries

    @property
    def input_factory(self) -> Callable[[TI], any]:
        return self._input_factory

    @input_factory.setter
    def input_factory(self, value):
        self._input_factory = value

    @property
    def output_factory(self) -> Callable[[TO], any]:
        return self._output_factory

    @output_factory.setter
    def output_factory(self, value):
        self._output_factory = value

    def create_input(self, value: TI, *args) -> TI:
        if not isinstance(value, tuple):
            value = (value,)
        try:
            return self.input_factory(*value, *args)
        except Exception as exc:
            exc_msg = traceback.format_tb(exc.__traceback__)
            raise Exception(f"Error: Input creation error. Input values:{[*value, *args]} , exc_msg: {exc_msg}")

    def create_output(self, value: TO, *args) -> TO:
        if not isinstance(value, tuple):
            value = (value,)
        try:
            return self.output_factory(*value, *args)
        except Exception as exc:
            exc_msg = traceback.format_tb(exc.__traceback__)
            raise Exception(f"Error: Output creation error. Input values:{[*value, *args]} , exc_msg: {exc_msg}")

    def execute(self, request_object: TI) -> ResponseObject[TO]:
        try:
            input_object = self.create_input(request_object)
            return self.process_request(input_object)
        except Exception as exc:
            self.handle_exception(exc)
            return self.create_response(success=False)

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
            except Exception as loc_exc:
                exc_msg = traceback.format_tb(exc.__traceback__)
                self.logger.error(f"Error: Something went wrong with exception_handler: {handler}, exc_msg: {exc_msg}")

    def record_event(self, event: IEvent):
        for recorder in self.event_recorders:
            recorder.record_event(event)

    def create_response(self, msg: TO = None, success=True) -> ResponseObject[TO]:
        return ResponseObject(success=success, msg=msg)

    def create_present_output(self, *args):
        if len(args) == 0:
            args = ((),)
        output_dto = self.create_output(*args)
        self.present_output_boundary(output_dto)
        return self.create_response(msg=output_dto)
