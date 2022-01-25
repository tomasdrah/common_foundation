import pytest

from common_foundation.domain.use_case_base.use_case_base import UseCaseBase


def test_use_case_base():
    with pytest.raises(TypeError):
        use_case = UseCaseBase()
        # use_case.execute((10, 11))

