from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, List, Any, Set

from memory.State import State


@dataclass
class BaseAlgorithm(ABC):
    frontier: ClassVar[List[State]] = field(default=[])
    closed_list: ClassVar[Set[State]] = field(default=set())

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
