import logging

import numpy as np
import pytest

from algorithms.BFS import BFS
from memory.State import State

logging.basicConfig(level=logging.DEBUG)


class TestAlgorithms:
    @pytest.fixture
    def some_state(self):
        example_state: State = State(
            state=np.array(
                [[2, 0, 3, 6], [1, 9, 7, 8], [14, 10, 15, 12], [5, 13, 11, 4]]
            )
        )
        yield example_state

    def test_bfs(self, some_state):
        bfs = BFS("UDLR")
        solution: str = bfs.solve(some_state)
