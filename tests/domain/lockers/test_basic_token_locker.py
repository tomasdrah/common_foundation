from datetime import datetime

from common_foundation.domain.lockers.basic_token_locker import BasicTokenLocker


def test_token_locker():
    start = datetime.now()

    # lock = ITokenLocker[int]()
    lock = BasicTokenLocker(current_token=255, max_wait_s=0.1)
    first_id = lock.get_new_access_id()
    a = 0
    with lock.get(access_id=first_id):
        old_token = lock.get_token()
        assert old_token == 255
        lock.set_new_token(125)
        assert lock.get_token() == 125

        with lock.get(access_id=first_id):
            lock.set_new_token(125)
            assert lock.get_token() == 125

        with lock.get(lock.get_new_access_id()):
            lock.set_new_token(10)
            assert lock.get_token() == 10

        with lock.get(first_id):
            lock.set_new_token(100)
            assert lock.get_token() == 100

    with lock.get(first_id):
        lock.set_new_token(10)
        assert lock.get_token() == 10

    end = datetime.now()
    duration = end - start
    dur_sec = duration.microseconds/1000000
    assert dur_sec < 0.3
