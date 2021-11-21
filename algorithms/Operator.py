from typing import Tuple

import numpy as np


class Operator:
    @classmethod
    def up(cls, start_state: np.array) -> np.array:
        pass

    @classmethod
    def down(cls, start_state) -> np.array:
        pass

    @classmethod
    def left(cls, start_state) -> np.array:
        return np.copy(start_state)

    @classmethod
    def right(cls, start_state) -> np.array:
        pass

    @classmethod
    def _find_empty(cls, state: np.array) -> Tuple[int]:
        """Return zero-based coordinates for empty tile as a tuple (<row>, <column>)"""
        return np.where(state == 0)[0]
