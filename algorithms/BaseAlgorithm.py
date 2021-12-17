from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import Queue
from typing import Any, Dict

from memory.State import State


@dataclass
class BaseAlgorithm(ABC):
    frontier: Queue[State] = field(default=Queue(maxsize=0))
    closed_list: Dict[int, State] = field(
        default_factory=dict
    )  # mapping {hash(state): state}

    @staticmethod
    @abstractmethod
    def solve(state: State) -> str:
        """
        A method implementing the algorithm, which returns a solution for a given puzzle.

        :param state: input puzzle to solve
        :return: a list of operations that leads to solving the puzzle as a string of characters
        symbolising four possible directions of moves L(EFT)|R(IGHT)|U(P)|D(OWN) i.e. "URRULDU"
        """
        pass

    @staticmethod
    @abstractmethod
    def visualize_solution() -> Any:
        # TODO: maybe
        pass
