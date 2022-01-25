import threading
import uuid
from datetime import datetime
from typing import Optional, Generic, TypeVar

from common_foundation.domain.lockers.i_token_locker import ITokenLocker, ITokenLockerWhile

T = TypeVar('T')


class BasicTokenLocker(Generic[T], ITokenLocker[T]):
    def __init__(self, current_token: T, max_wait_s=30.0):
        self._lock = threading.Lock()
        self._id: None | int = self._reset_id()
        self._counter = 0
        self._locked_time = datetime.now()
        self.max_sec_lock = max_wait_s
        self._while = BasicTokenLockerWhile[T](self)
        self._current_token = current_token

    def get_new_access_id(self) -> int:
        return uuid.uuid4().int

    def get_token(self) -> T:
        return self._current_token

    def set_new_token(self, token: T):
        self._current_token = token

    def get(self, access_id: Optional[int]):
        return self._while.get(access_id)

    def acquire(self, id: Optional[int], blocking=True):
        if id:
            if self._remaining_time() == 0:
                self.release()
            if self._id != id:
                self._lock.acquire(blocking=blocking, timeout=self._remaining_time())
                self._locked_time = datetime.now()
                self._id = id
        self._counter += 1
        return True

    def _remaining_time(self):
        dif = datetime.now() - self._locked_time
        sec = self.max_sec_lock - dif.microseconds / 1000000
        if sec > 0:
            return sec
        return 0

    def release(self):
        self._counter = self._counter - 1 if self._counter > 0 else 0
        if self._counter == 0:
            self._reset_id()
            if self._lock.locked():
                self._lock.release()

    def _reset_id(self):
        self._id = None
        return None


class BasicTokenLockerWhile(Generic[T], ITokenLockerWhile[T]):
    def __init__(self, id_locker: BasicTokenLocker, id: int = None):
        self.locker = id_locker
        self.id = id

    def get(self, id: Optional[int]):
        instance = self.__class__(self.locker, id)
        return instance

    def __enter__(self):
        self.locker.acquire(self.id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.locker.release()


if __name__ == "__main__":
    lock = BasicTokenLocker(10)
    a = 0

    with lock.get(1):
        a = a
    with lock.get(1):
        with lock.get(1):
            a = a
        with lock.get(2):
            a = a
        a = a

    a = a
