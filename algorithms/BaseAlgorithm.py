from abc import ABC, abstractmethod
from dataclasses import field
from queue import Queue
from typing import Any, Dict

from memory.State import State


class BaseAlgorithm(ABC):
    max_depth: int
    visited_states: int
    frontier: Queue[State] = field(default_factory=Queue)
    closed_list: Dict[int, State] = field(
        default_factory=dict
    )  # mapping {hash(state): state}

    @staticmethod
    @abstractmethod
    def solve(self, state: State) -> str:
        """
        A method implementing the algorithm, which returns a solution for a given puzzle.

        :param state: input puzzle to solve
        :return: a list of operations that leads to solving the puzzle as a string of characters
        symbolising four possible directions of moves L(EFT)|R(IGHT)|U(P)|D(OWN) i.e. "URRULDU"
        """
        pass

    @abstractmethod
    def visualize_solution(self, state: State) -> Any:
        # TODO: maybe
        pass
