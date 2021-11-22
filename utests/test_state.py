import numpy as np
import pytest

from memory.State import State


class TestState:
    EXAMPLE_FRAME_PATH: str = "./Resources/ramka1_4x4.txt"

    @pytest.fixture
    def create_state(self):
        example_state: State = State(
            np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 11, 12], [13, 14, 15, 10]])
        )
        yield example_state

    @pytest.fixture
    def state_bottom_left_corner(self):
        example_state: State = State(
            np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [0, 14, 15, 13]])
        )
        yield example_state

    @pytest.fixture
    def state_top_right_corner(self):
        example_state: State = State(
            np.array([[1, 2, 3, 0], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 4]])
        )
        yield example_state

    def test_load_state(self):
        test_state = State.load_state(self.EXAMPLE_FRAME_PATH)
        assert type(test_state) is np.ndarray
        assert test_state.shape == (4, 4)

    def test_get_state_shape(self, create_state):
        test_state_shape = create_state.get_state_shape()
        assert type(test_state_shape) is tuple
        assert test_state_shape == (4, 4)

    def test__find_empty(self, create_state):
        test_state_index = create_state._find_zero()
        assert type(test_state_index) is tuple
        assert test_state_index == (2, 1)

    def test__swap_values(self, create_state):
        new_state_array = create_state._swap_values((2, 2))
        assert (
            new_state_array
            == np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 14, 15, 10]])
        ).all()

    def test_up(self, create_state):
        state_after_move = create_state.up()
        assert (
            state_after_move.state
            == np.array([[1, 2, 3, 4], [5, 0, 7, 8], [9, 6, 11, 12], [13, 14, 15, 10]])
        ).all()

    def test_down(self, create_state):
        state_after_move = create_state.down()
        assert (
            state_after_move.state
            == np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 14, 11, 12], [13, 0, 15, 10]])
        ).all()

    def test_left(self, create_state):
        state_after_move = create_state.left()
        assert (
            state_after_move.state
            == np.array([[1, 2, 3, 4], [5, 6, 7, 8], [0, 9, 11, 12], [13, 14, 15, 10]])
        ).all()

    def test_right(self, create_state):
        state_after_move = create_state.right()
        assert (
            state_after_move.state
            == np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 14, 15, 10]])
        ).all()

    def test__check_legal_move(self, state_top_right_corner, state_bottom_left_corner):
        pass
