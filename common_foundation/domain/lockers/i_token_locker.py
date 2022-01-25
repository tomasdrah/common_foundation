from typing import TypeVar, Generic

T = TypeVar('T')


class ITokenLockerWhile(Generic[T]):

    # freeze actual token for some time
    # wait for release if my access id isn't the released one, or it's not released
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class ITokenLocker(Generic[T]):
    def get(self, access_id: int) -> ITokenLockerWhile:
        raise NotImplementedError

    # optional way how to get new id
    def get_new_access_id(self) -> int:
        raise NotImplementedError

    # anyone can return actual token
    def get_token(self) -> T:
        raise NotImplementedError

    # anyone can return actual token
    def set_new_token(self, token: T):
        raise NotImplementedError
