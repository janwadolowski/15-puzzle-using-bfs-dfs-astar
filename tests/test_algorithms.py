import numpy as np
import pytest

from memory.State import State


class TestAlgorithms:
    @pytest.fixture
    def some_state(self):
        example_state: State = State(
            state=np.array(
                [[2, 0, 3, 6], [1, 9, 7, 8], [14, 10, 15, 12], [5, 13, 11, 4]]
            )
        )
        yield example_state

    def test_sth(self):
        pass
