import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, List, Tuple

import numpy as np


@dataclass
class State:
    state: np.array
    parent: Optional[np.array] = None
    preceding_operator: Optional[Callable] = None

    def up(self) -> np.array:

        pass

    def down(self) -> np.array:
        pass

    def left(self) -> np.array:
        return np.copy(self.state)

    def right(self) -> np.array:
        pass

    def _find_empty(self) -> int:
        """ Return position of 0 in the array"""

    @classmethod
    def load_state(cls, filepath: str) -> np.array:
        filepath_ = Path(filepath)
        try:
            with open(filepath_, 'r') as f:
                # Get rid of 1st line, which is size
                _, *output_str = f.readlines()  # ['1 2 3 4', '5 6 7 8', '9 10 11 12', '13 14 15 0']
                output_list_str: List[List[str]] = [line.strip('\n').split(sep=' ') for line in output_str]
                # [[ '5',  '6',  '7',  '8'],
                #  [ '9', '10', '11', '12'],
                #  ['13', '14', '15',  '0']]
                return np.array(output_list_str)
        except Exception as e:
            logging.error(e)
            raise e

    @classmethod
    def load_state_shape(cls, filepath: str) -> Tuple[int]:
        filepath_ = Path(filepath)
        try:
            with open(filepath_, 'r') as f:
                # Get rid of 1st line, which is size
                output_str = f.readline()
                return tuple([int(char) for char in output_str.strip('\n').split(' ')])
        except Exception as e:
            logging.error(e)
            raise e

    def __init__(self, start_state: np.array, operator: Callable):
        self.state = operator(start_state)
        self.parent = start_state
        self.preceding_operator = operator
