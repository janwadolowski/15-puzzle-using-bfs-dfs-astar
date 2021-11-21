import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, List, Tuple

import numpy as np


@dataclass
class State:
    state: np.ndarray
    parent: Optional["State"] = None
    preceding_operator: Optional[Callable] = None

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

    @staticmethod
    def up(start_state: "State") -> [np.ndarray]:
        """Get a State and return a new one"""
        coords_change = (0, 1)
        if start_state._check_legal_move(coords_change):
            return
        else:
            return

    @staticmethod
    def down(start_state) -> np.array:
        pass

    @staticmethod
    def left(start_state) -> np.array:
        return np.copy(start_state)

    @staticmethod
    def right(start_state) -> np.array:
        pass

    def _find_zero(self) -> Tuple[int, int]:
        """Return zero-based coordinates for empty tile as a tuple (<row>, <column>)"""
        return np.where(self.state == 0)[
            0
        ]  # Returns a list of all matches, so we only take the first match, since there's only 1 zero anyway

    def _check_legal_move(self, change: Tuple[int, int]) -> bool:
        """Returns True if the operation up | down | left | right is valid else False"""

        def sum_tuples(first: Tuple[int, int], second: Tuple[int, int]):
            """Defines operation: (a, b) + (c, d) = (a+b, c+d)"""
            return (first[0] + second[0], first[1] + second[1])

        zero_coords: Tuple[int, int] = self._find_zero()
        summed: Tuple[int, int] = sum_tuples(self._find_zero(), change)

        if summed[0] < 0 or summed[0] > self.state.shape[0]:
            return False
        elif summed[1] < 0 or summed[1] > self.state.shape[1]:
            return False
        else:
            return True
