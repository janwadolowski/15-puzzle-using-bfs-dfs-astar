import numpy as np

from memory.State import State


class TestState:
    def test_load_state(self):
        test_state = State.load_state('./Resources/ramka1_4x4.txt')
        assert type(test_state) is np.ndarray
        assert test_state.shape == (4, 4)

    def test_load_state_shape(self):
        test_state_shape = State.load_state_shape('./Resources/ramka1_4x4.txt')
        assert type(test_state_shape) is tuple
        assert len(test_state_shape) == 2
