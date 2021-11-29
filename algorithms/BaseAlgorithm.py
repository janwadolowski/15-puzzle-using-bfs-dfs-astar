from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, List, Dict, Any

from memory.State import State


@dataclass
class BaseAlgorithm(ABC):
    frontier: ClassVar[List[State]] = field(default=[])
    closed_list: ClassVar[Dict[State, List[State]]] = field(default={})

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
    def visualize_solution(self) -> Any:
        # TODO: maybe
        pass
