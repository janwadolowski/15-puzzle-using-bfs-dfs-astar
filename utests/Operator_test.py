import numpy as np
import pytest

from algorithms.Operator import Operator


class TestState:
    @pytest.fixture()
    def setup_class(cls):
        test_state = np.ndarray(
            [[1, 3, 4, 8],
             [2, 6, 9, 7],
             [5, 15, 10, 11],
             [0, 14, 12, 13]]
        )

    def test__find_empty(self):
        test_state_index = Operator._find_empty(TestState.test_state)
        assert type(test_state_index) is tuple
        assert test_state_index == (3, 0)
