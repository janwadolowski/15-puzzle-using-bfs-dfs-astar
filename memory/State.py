import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple, Final

# noinspection Mypy
import numpy as np

from Exception import InvalidCoordinatesException


@dataclass
class State:
    state: np.ndarray
    parent: Optional["State"] = None
    preceding_operator: Optional[str] = None

    @staticmethod
    def load_state(filepath: str) -> np.array:
        filepath_ = Path(filepath)
        try:
            with open(filepath_, "r") as f:
                # Get rid of 1st line, which is size
                (
                    _,
                    *output_str,
                ) = f.readlines()  # ['1 2 3 4', '5 6 7 8', '9 10 11 12', '13 14 15 0']
                output_list_str: List[List[str]] = [
                    line.strip("\n").split(sep=" ") for line in output_str
                ]
                # [[ '5',  '6',  '7',  '8'],
                #  [ '9', '10', '11', '12'],
                #  ['13', '14', '15',  '0']]
                return np.array(output_list_str)
        except Exception as e:
            logging.error(e)
            raise e

    def get_state_shape(self) -> Tuple[int, int]:
        return self.state.shape

    def up(self) -> Optional["State"]:
        """Get a State and return a new one with 0 moved up or None if a move is illegal"""
        return self._move("up")

    def down(self) -> Optional["State"]:
        """Get a State and return a new one with 0 moved down or None if a move is illegal"""
        return self._move("down")

    def left(self) -> Optional["State"]:
        """Get a State and return a new one with 0 moved left or None if a move is illegal"""
        return self._move("left")

    def right(self) -> "State":
        """Get a State and return a new one with 0 moved right or None if a move is illegal"""
        return self._move("right")

    def _find_zero(self) -> Tuple[int, int]:
        """Return zero-based coordinates for 0 tile as a tuple (<row>, <column>)"""
        a, b = np.where(self.state == 0)
        return int(a), int(b)  # Explicit casting for mypy

    @staticmethod
    def _sum_tuples(first: Tuple[int, int], second: Tuple[int, int]):
        """Defines operation: (a, b) + (c, d) = (a+b, c+d)"""
        return first[0] + second[0], first[1] + second[1]

    def _check_legal_move(self, change: Tuple[int, int]) -> bool:
        """Returns True if the operation up | down | left | right is valid else False"""
        zero_coords: Tuple[int, int] = self._find_zero()
        summed: Tuple[int, int] = self._sum_tuples(zero_coords, change)

        rows_len, columns_len = self.state.shape

        if summed[0] < 0 or summed[0] >= columns_len:
            return False
        elif summed[1] < 0 or summed[1] >= rows_len:
            return False
        else:
            return True

    def _swap_values(self, swap_with: Tuple[int, int]) -> np.ndarray:
        """
        Return a new ndarray with swapped values

        :param swap_with: a tuple with indexes of to swap 0 with
        """
        a: Tuple[int, int] = self._find_zero()
        b: Tuple[int, int] = swap_with  # for better legibility

        coords_diff: Tuple[int, int] = self._sum_tuples(a, (-b[0], -b[1]))
        coords_diff = (abs(coords_diff[0]), abs(coords_diff[1]))
        # Can only move 1 index in any direction, if coords are too far apart raise an error
        if coords_diff not in [(0, 1), (1, 0)]:
            raise InvalidCoordinatesException("Coordinates are too far from each other")
        else:
            swapped = np.copy(self.state)
            # a, b = b, a -- this works in python as intended, ie. swaps both values
            swapped[a], swapped[b] = swapped[b], swapped[a]
            return swapped

    def _move(self, direction: str) -> Optional["State"]:
        direction_coords: tuple[int, int] | None = None
        match direction:
            case "up":
                direction_coords = (-1, 0)
            case "down":
                direction_coords = (1, 0)
            case "left":
                direction_coords = (0, -1)
            case "right":
                direction_coords = (0, 1)

        # If valid direction and the move is legal (within the state array boundaries) proceed
        if direction_coords and self._check_legal_move(direction_coords):
            new_coords: tuple[int, int] = State._sum_tuples(
                self._find_zero(), direction_coords
            )
            new_state_array: np.ndarray = self._swap_values(new_coords)
            logging.debug(
                f"_move executed with direction={direction}, direction_coords={direction_coords}, new_coords={new_coords}, new_state_array={new_state_array}"
            )
            return State(
                state=new_state_array, parent=self, preceding_operator=direction
            )
        else:
            logging.debug(f"_move")
            return None

    def get_neighbors(self) -> List["State"]:
        available_moves: List[State] = []
        for move in [self.left, self.right, self.up, self.down]:
            if available := move():
                available_moves.append(available)
        return available_moves

    def is_target_state(self) -> bool:
        target_state: Final = State(
            state=np.array(
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
            )
        )
        return self == target_state

    def __eq__(self, other: "State"):
        if isinstance(other, self.__class__) and (self.state == other.state).all():
            return True
        else:
            return False

    def __deepcopy__(self, memo=None) -> "State":
        # TODO do we need this?
        """
        Method to deep copy an object.

        It's not a full deep copy as for the purpose of the algorithm
        we only need to deep copy the state (numpy.ndarray)
        but we can only reference the parent state.

        :return: A deep copy of an object with referenced parent state
        """
        if not memo:
            memo = {}
        return State(
            state=self.state.copy(),
            parent=self.parent,  # This in only referenced, not copied
            preceding_operator=self.preceding_operator,
        )
