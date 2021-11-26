from typing import Tuple

import numpy as np
import pytest
from pytest_mock import MockerFixture

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

    def test_create_state(self):
        parent_array = np.array(
            [[10, 9, 8, 0], [15, 14, 13, 7], [12, 11, 6, 5], [4, 3, 2, 1]]
        )
        child_array = np.array(
            [[10, 9, 8, 7], [15, 14, 13, 0], [12, 11, 6, 5], [4, 3, 2, 1]]
        )
        test_parent_state = State(state=parent_array)
        test_state = State(
            state=child_array,
            parent=test_parent_state,
            preceding_operator="down",
        )

        assert (test_parent_state.state == parent_array).all()
        assert test_parent_state.preceding_operator is None
        assert test_parent_state.parent is None

        assert (test_state.state == child_array).all()
        assert test_state.preceding_operator == "down"
        assert test_state.parent is test_parent_state

    def test_load_state(self):
        test_state = State.load_state(self.EXAMPLE_FRAME_PATH)
        assert type(test_state) is np.ndarray
        assert test_state.shape == (4, 4)

    def test_get_state_shape(self, create_state: State):
        test_state_shape = create_state.get_state_shape()
        assert type(test_state_shape) is tuple
        assert test_state_shape == (4, 4)

    def test__find_zero(self, create_state: State):
        test_state_index = create_state._find_zero()
        assert type(test_state_index) is tuple
        assert test_state_index == (2, 1)

    def test__swap_values(self, create_state: State):
        # [[1, 2, 3, 4],           [[1, 2, 3, 4],
        #  [5, 6, 7, 8],      =>    [5, 6, 7, 8],
        #  [9, 0, 11, 12],          [9, 11, 0, 12],
        #  [13, 14, 15, 10]]        [13, 14, 15, 10]]
        new_state_array = create_state._swap_values((2, 2))
        assert (
            new_state_array
            == np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 14, 15, 10]])
        ).all()

    def test_up(self, create_state: State, mocker: MockerFixture):
        # [[1, 2, 3, 4],           [[1, 2, 3, 4],
        #  [5, 6, 7, 8],      =>    [5, 0, 7, 8],
        #  [9, 0, 11, 12],          [9, 6, 11, 12],
        #  [13, 14, 15, 10]]        [13, 14, 15, 10]]

        # Patch internal function
        new_state_mocked = State(
            state=np.array(
                [[1, 2, 3, 4], [5, 0, 7, 8], [9, 6, 11, 12], [13, 14, 15, 10]]
            ),
            parent=create_state,
            preceding_operator="up",
        )
        move_patch = mocker.patch(
            target="memory.State.State._move", return_value=new_state_mocked
        )

        new_state = create_state.up()

        # Assertions
        move_patch.assert_called_once_with("up")
        assert new_state == new_state_mocked

    def test_down(self, create_state: State, mocker: MockerFixture):
        # [[1, 2, 3, 4],           [[1, 2, 3, 4],
        #  [5, 6, 7, 8],      =>    [5, 6, 7, 8],
        #  [9, 0, 11, 12],          [9, 14, 11, 12],
        #  [13, 14, 15, 10]]        [13, 0, 15, 10]]

        # Patch internal function
        new_state_mocked = State(
            state=np.array(
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 14, 11, 12], [13, 0, 15, 10]]
            ),
            parent=create_state,
            preceding_operator="down",
        )
        move_patch = mocker.patch(
            target="memory.State.State._move", return_value=new_state_mocked
        )

        new_state = create_state.down()

        # Assertions
        move_patch.assert_called_once_with("down")
        assert new_state == new_state_mocked

    def test_left(self, create_state: State, mocker: MockerFixture):
        # [[1, 2, 3, 4],           [[1, 2, 3, 4],
        #  [5, 6, 7, 8],      =>    [5, 6, 7, 8],
        #  [9, 0, 11, 12],          [0, 9, 11, 12],
        #  [13, 14, 15, 10]]        [13, 14, 15, 10]]

        # Patch internal function
        new_state_mocked = State(
            state=np.array(
                [[1, 2, 3, 4], [5, 6, 7, 8], [0, 9, 11, 12], [13, 14, 15, 10]]
            ),
            parent=create_state,
            preceding_operator="left",
        )
        move_patch = mocker.patch(
            target="memory.State.State._move", return_value=new_state_mocked
        )

        new_state = create_state.left()

        # Assertions
        move_patch.assert_called_once_with("left")
        assert new_state == new_state_mocked

    def test_right(self, create_state: State, mocker: MockerFixture):
        # [[1, 2, 3, 4],           [[1, 2, 3, 4],
        #  [5, 6, 7, 8],      =>    [5, 6, 7, 8],
        #  [9, 0, 11, 12],          [9, 11, 0, 12],
        #  [13, 14, 15, 10]]        [13, 14, 15, 10]]

        # Patch internal function
        new_state_mocked = State(
            state=np.array(
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 14, 15, 10]]
            ),
            parent=create_state,
            preceding_operator="right",
        )
        move_patch = mocker.patch(
            target="memory.State.State._move", return_value=new_state_mocked
        )

        new_state = create_state.right()

        # Assertions
        move_patch.assert_called_once_with("right")
        assert new_state == new_state_mocked

    # All coords changes combinations with expected test results for top right corner 0 and bottom left corner 0
    testdata_top_right_corner = [
        ((0, 3), (1, 0), (1, 3), True),  # Movement down
        ((0, 3), (0, 1), (0, 4), False),  # Movement right
        ((0, 3), (-1, 0), (-1, 3), False),  # Movement up
        ((0, 3), (0, -1), (0, 2), True),  # Movement left
    ]

    @pytest.mark.parametrize(
        "mocked_zero_coords, change, mocked_sum, expected", testdata_top_right_corner
    )
    def test__check_legal_move_top_right_corner(
        self,
        state_top_right_corner: State,
        mocker: MockerFixture,
        mocked_zero_coords,
        change,
        mocked_sum,
        expected,
    ):
        # Mocks
        find_zero_patch = mocker.patch(
            target="memory.State.State._find_zero", return_value=mocked_zero_coords
        )
        sum_tuples_patch = mocker.patch(
            target="memory.State.State._sum_tuples", return_value=mocked_sum
        )
        result = state_top_right_corner._check_legal_move(change)

        # Assertions
        find_zero_patch.assert_called_once()
        sum_tuples_patch.assert_called_once_with(mocked_zero_coords, change)
        assert result == expected

    testdata_bottom_left_corner = [
        ((3, 0), (1, 0), (4, 0), False),  # Movement down
        ((3, 0), (0, 1), (3, 1), True),  # Movement right
        ((3, 0), (-1, 0), (2, 0), True),  # Movement up
        ((3, 0), (0, -1), (3, -1), False),  # Movement left
    ]

    @pytest.mark.parametrize(
        "mocked_zero_coords, change, mocked_sum, expected", testdata_bottom_left_corner
    )
    def test__check_legal_move_bottom_left_corner(
        self,
        state_bottom_left_corner: State,
        mocker: MockerFixture,
        mocked_zero_coords,
        change,
        mocked_sum,
        expected,
    ):
        # Mocks
        find_zero_patch = mocker.patch(
            target="memory.State.State._find_zero", return_value=mocked_zero_coords
        )
        sum_tuples_patch = mocker.patch(
            target="memory.State.State._sum_tuples", return_value=mocked_sum
        )
        result = state_bottom_left_corner._check_legal_move(change)

        # Assertions
        find_zero_patch.assert_called_once()
        sum_tuples_patch.assert_called_once_with(mocked_zero_coords, change)
        assert result == expected

    directions_and_coords = [
        (
            "up",
            (-1, 0),
            (1, 1),
            np.array([[1, 2, 3, 4], [5, 0, 7, 8], [9, 6, 11, 12], [13, 14, 15, 10]]),
        ),
        (
            "down",
            (1, 0),
            (3, 1),
            np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 14, 11, 12], [13, 0, 15, 10]]),
        ),
        (
            "left",
            (0, -1),
            (2, 0),
            np.array([[1, 2, 3, 4], [5, 6, 7, 8], [0, 9, 11, 12], [13, 14, 15, 10]]),
        ),
        (
            "right",
            (0, 1),
            (2, 2),
            np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 14, 15, 10]]),
        ),
    ]

    @pytest.mark.parametrize(
        "direction, direction_coords, new_coords, swapped_array", directions_and_coords
    )
    def test__move_legal(
        self,
        create_state: State,
        mocker: MockerFixture,
        direction: str,
        direction_coords: Tuple[int, int],
        new_coords: Tuple[int, int],
        swapped_array: np.ndarray,
    ):
        # Mocks
        swapped_state = State(
            state=swapped_array, parent=create_state, preceding_operator=direction
        )
        check_legal_move_patch = mocker.patch(
            target="memory.State.State._check_legal_move", return_value=True
        )
        find_zero_patch = mocker.patch(
            target="memory.State.State._find_zero", return_value=(2, 1)
        )
        swap_values_patch = mocker.patch(
            target="memory.State.State._swap_values", return_value=swapped_array
        )

        new_state: State = create_state._move(direction)

        # Assertions
        check_legal_move_patch.assert_called_once_with(direction_coords)
        find_zero_patch.assert_called_once()
        swap_values_patch.assert_called_once_with(new_coords)
        assert new_state == swapped_state

    directions_and_coords = [
        ("down", (1, 0), (3, 1)),
        ("left", (0, -1), (2, 0)),
    ]

    @pytest.mark.parametrize(
        "direction, direction_coords, new_coords", directions_and_coords
    )
    def test__move_illegal(
        self,
        state_bottom_left_corner: State,
        mocker: MockerFixture,
        direction: str,
        direction_coords: Tuple[int, int],
        new_coords: Tuple[int, int],
    ):
        # Mocks
        check_legal_move_patch = mocker.patch(
            target="memory.State.State._check_legal_move", return_value=False
        )
        sum_tuples_patch = mocker.patch(target="memory.State.State._sum_tuples")
        find_zero_patch = mocker.patch(target="memory.State.State._find_zero")
        swap_values_patch = mocker.patch(target="memory.State.State._swap_values")

        new_state: State = state_bottom_left_corner._move(direction)

        # Assertions
        check_legal_move_patch.assert_called_once_with(direction_coords)
        sum_tuples_patch.assert_not_called()
        find_zero_patch.assert_not_called()
        swap_values_patch.assert_not_called()
        assert new_state is None

    adding_tuples = [
        ((2, 3), (0, 1), (2, 4)),
        ((3, 1), (1, 0), (4, 1)),
        ((2, 2), (0, -1), (2, 1)),
        ((1, 1), (-1, 0), (0, 1)),
        ((3, 3), (1, -2), (4, 1)),
    ]

    @pytest.mark.parametrize("first, second, expected", adding_tuples)
    def test__sum_tuples(
        self, first: Tuple[int, int], second: Tuple[int, int], expected: Tuple[int, int]
    ):
        assert State._sum_tuples(first, second) == expected

    def test_get_available_moves(
        self,
        create_state: State,
        state_bottom_left_corner: State,
        state_top_right_corner: State,
        mocker: MockerFixture,
    ):
        move_patch = mocker.patch(
            target="memory.State.State._move", return_value=None
        )
        assert create_state.get_available_moves() == [State(state=np.array([[1, 2, 3, 4], [5, 0, 7, 8], [9, 6, 11, 12], [13, 14, 15, 10]]))]


        # TODO: Write a test
        pass
