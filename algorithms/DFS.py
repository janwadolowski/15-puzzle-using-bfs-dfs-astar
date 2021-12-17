from typing import Any

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class DFS(BaseAlgorithm):
    """A class for Depth First Search algorithm initialised with algorithm parameters."""

    neighbors_quality_order: str
    depth: int

    def solve(self, start: State) -> str:
        pass

    def visualize_solution(self) -> Any:
        pass
