from typing import TypeVar, Generic

TO = TypeVar('TO')


class ResponseObject(Generic[TO]):
    def __init__(self, success: bool, msg: TO = None):
        self.success = success
        self.msg = msg

    def __bool__(self):
        return self.success
