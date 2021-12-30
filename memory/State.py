from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Literal, Optional, Tuple, TypeAlias

# noinspection Mypy
import numpy as np
from loguru import logger

from Exception import InvalidCoordinatesException

DIRECTION: TypeAlias = Literal["left", "right", "up", "down"]


@dataclass
class State:
    array: np.ndarray
    heuristic_value: int | None = None
    parent: Optional["State"] = None
    preceding_operator: DIRECTION | None = None

    def __post_init__(self):
        self.operations_str_mapping: Dict[str, Callable] = {
            "L": self.left,
            "R": self.right,
            "U": self.up,
            "D": self.down,
        }

    @property
    def target_state(self):
        return self._generate_target_state()

    @staticmethod
    def load_state(filepath: str) -> Optional["State"]:
        """
        Load initial State for 15 puzzle from a file.

        :param filepath: Path to txt file the with initial State
        :return: A loaded State or None if the operation failed.
        """
        # TODO: Add :raise <Exception>: docstring
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
                array_of_str = np.array(output_list_str)
                array_of_int = array_of_str.astype(np.int32)
                return State(
                    array=array_of_int,
                    parent=None,
                )
        except IOError as e:
            logger.error(e)
            raise e

    def get_state_shape(self) -> Tuple[int, int]:
        return self.array.shape

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
        a, b = np.where(self.array == 0)
        return int(a), int(b)  # Explicit casting for mypy

    @staticmethod
    def _sum_tuples(first: Tuple[int, int], second: Tuple[int, int]):
        """Defines operation: (a, b) + (c, d) = (a+b, c+d)"""
        return first[0] + second[0], first[1] + second[1]

    @staticmethod
    def _diff_tuples(
        first: Tuple[int, int], second: Tuple[int, int]
    ) -> Tuple[int, int]:
        """
        Calculates difference in coordinates between two tuples as a tuple with coordinates distance like so:
        (a, b), (c, d) -> ( abs(c-a), abs(d-b) )

        _diff_tuples( (2, 3), (1, 1) ) -> (1, 2)
        """
        return abs(second[0] - first[0]), abs(second[1] - first[1])

    @staticmethod
    def diff_coords(start: tuple[int, int], target: tuple[int, int]) -> int:
        """Calculate a "distance" between two coords, i.e. how many moves are required at least to move a tyle from a(x, y) to b(p, q)."""
        diff: tuple[int, int] = State._diff_tuples(start, target)
        return diff[0] + diff[1]

    def find_coords(self, tile: int) -> tuple[int, int] | None:
        """Find coords of selected tile in a State."""
        try:
            return (
                np.where(self.array == tile)[0][0],
                np.where(self.array == tile)[1][0],
            )  # coords are described per each subarray separately
        except IndexError:
            logger.error(f"Coords for tile {tile} not found.")
            return None

    def _check_legal_move(self, change: Tuple[int, int]) -> bool:
        """Returns True if the operation up | down | left | right is valid else False"""
        zero_coords: Tuple[int, int] = self._find_zero()
        summed: Tuple[int, int] = self._sum_tuples(zero_coords, change)

        rows_len, columns_len = self.array.shape

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
            logger.error(
                f"Coordinates {a} and {b} are too far from each other to swap."
            )
            raise InvalidCoordinatesException(
                "Coordinates are too far from each other to swap."
            )
        else:
            swapped = np.copy(self.array)
            # a, b = b, a -- this works in python as intended, i.e. swaps both values
            swapped[a], swapped[b] = swapped[b], swapped[a]
            return swapped

    def _move(self, direction: DIRECTION) -> Optional["State"]:
        """
        Return a new State with 0 moved in a direction passed as parameter. If move is not possible return None.

        :param direction: one of: "left" | "right" | "up" | "down"
        :return: new State with zero moved in a specified direction or None if a move is illegal.
        """
        direction_coords: Tuple[int, int] | None = None
        match direction:
            case "left":
                direction_coords = (0, -1)
            case "right":
                direction_coords = (0, 1)
            case "up":
                direction_coords = (-1, 0)
            case "down":
                direction_coords = (1, 0)

        # If valid direction and the move is legal (within the State array boundaries) proceed
        if direction_coords and self._check_legal_move(direction_coords):
            new_coords: tuple[int, int] = State._sum_tuples(
                self._find_zero(), direction_coords
            )
            new_state_array: np.ndarray = self._swap_values(new_coords)
            logger.debug(
                f"_move executed with direction={direction}, direction_coords={direction_coords}, new_coords={new_coords}, new_state_array=\n{new_state_array}"
            )
            return State(
                array=new_state_array, parent=self, preceding_operator=direction
            )
        else:
            logger.debug(
                f"attempted move from coords: {self._find_zero()} in illegal direction: {direction}."
            )
            return None

    def get_neighbors(self, neighbors_query_order: str) -> List["State"]:
        available_moves: List[State] = []
        for direction in neighbors_query_order:
            if available := self.operations_str_mapping[
                direction
            ]():  # iterate over "LRUD" and call function mapped to direction, e.g. {"U": self.up}
                available_moves.append(available)
        return available_moves

    def _generate_target_state(self) -> "State":
        """
        Method to create a target State (i.e. a 2D array with consecutive numbers 1...n-1 and 0 at the end) based on object's array.

        An example target state for 4x4 array:
        [[ 1,  2,  3,  4],
         [ 5,  6,  7,  8],
         [ 9, 10, 11, 12],
         [13, 14, 15,  0]]
        """
        num_range = len(self.array.flat)  # how many numbers are
        target_state = np.arange(
            1, num_range + 1
        )  # first create a 1D array 1...n (n is length of a flattened array we compare with)
        target_state[
            num_range
        ] = 0  # replace last value with 0 symbolising an empty tile
        target_state.reshape(
            self.array.shape
        )  # reshape the 1D array of consecutive numbers with 0 at the end to match the shape of array we compare with
        return State(array=target_state)

    def is_target_state(self) -> bool:
        return self == self.target_state

    def get_path_to_state(self, path_to_state: List[str] = None) -> str:
        """Get a list of operations required to reach a current State from the first State (i.e. State without a parent)"""
        if path_to_state is None:
            path_to_state = []
        if (
            self.preceding_operator is None
        ):  # If node doesn't have a parent it means it's the root (initial) node,which signals end of recursion
            path_to_state.reverse()  # Because moves are listed last to first, and we want first to last
            return "".join(path_to_state)
        else:
            path_to_state.append(self.preceding_operator[0].upper())
            return self.parent.get_path_to_state(path_to_state)

    def get_state_depth(self) -> int:
        """Get State's depth."""
        if (
            self.parent is None
        ):  # If node doesn't have a parent it means it's the root (initial) node,which signals end of recursion
            return 0
        else:
            return self.parent.get_state_depth() + 1

    def __hash__(self) -> int:
        return hash(self.array.tobytes())

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return (self.array == other.array).all()

    def __deepcopy__(self, memo=None) -> "State":
        """
        Method to deep copy an object.

        It's not a full deep copy as for the purpose of the algorithm
        we only need to deep copy the array (numpy.ndarray)
        but we can only reference the parent State.

        :return: A deep copy of an object with referenced parent array
        """
        # TODO: how to handle memo properly?
        if not memo:
            memo = {}
        return State(
            array=self.array.copy(),
            parent=self.parent,  # This in only referenced, not copied
        )
