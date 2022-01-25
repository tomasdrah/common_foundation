from common_foundation.domain.callable_object import BasicCallableObject


def dummy_fce_1(data: int):
    return data + 1


def dummy_fce_2(data: int):
    return data - 1


def test_basic_callable_object():
    callable_fce = BasicCallableObject.create_from_fce(dummy_fce_1)
    assert callable_fce.call(10) == 11

    callable_fce = BasicCallableObject(dummy_fce_1)
    assert callable_fce(10) == 11

    callable_fce.change_fce(dummy_fce_2)
    assert callable_fce(10) == 9
