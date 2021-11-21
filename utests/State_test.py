import numpy as np

from memory.State import State


class TestState:
    example_state = np.array(
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    )

    def test_load_state(self):
        test_state = State.load_state("./Resources/ramka1_4x4.txt")
        assert type(test_state) is np.ndarray
        assert test_state.shape == (4, 4)

    def test_load_state_shape(self):
        test_state_shape = self.example_state
        assert type(test_state_shape) is tuple
        assert test_state_shape == (4, 4)
