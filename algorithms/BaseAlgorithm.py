from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import Queue
from typing import Any, ClassVar, List

from memory.State import State


@dataclass
class BaseAlgorithm(ABC):
    neighbors_query_order: str
    frontier: ClassVar[List[State]] = field(default=[])
    closed_list: [Queue[State]] = field(default=Queue(maxsize=0))

    @staticmethod
    @abstractmethod
    def solve(state: State) -> List[str]:
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
