from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import Queue
from typing import Any, List

from memory.State import State


@dataclass
class BaseAlgorithm(ABC):
    frontier: Queue[State] = field(default=Queue(maxsize=0))
    closed_list: Queue[State] = field(default=Queue(maxsize=0))

    @staticmethod
    @abstractmethod
    def solve(state: State) -> str:
        """
        A method implementing the algorithm, which returns a solution for a given puzzle.

        :param state: input puzzle to solve
        :return: a list of operations that leads to solving the puzzle ie. ["up", "right", "right", "up"]
        """
        pass

    @staticmethod
    @abstractmethod
    def visualize_solution() -> Any:
        # TODO: maybe
        pass
