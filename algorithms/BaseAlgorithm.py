from abc import ABC, abstractmethod

from memory.State import State


class BaseAlgorithm(ABC):
    @abstractmethod
    def solve(self, state: State) -> str:
        """
        A method implementing the algorithm, which returns a solution for a given puzzle.

        :param state: input puzzle to solve
        :return: a list of operations that leads to solving the puzzle as a string of characters
        symbolising four possible directions of moves L(EFT)|R(IGHT)|U(P)|D(OWN) i.e. "URRULDU"
        """
        pass
