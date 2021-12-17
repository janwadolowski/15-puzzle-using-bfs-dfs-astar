import queue
from dataclasses import field
import copy
from typing import Any, List, Optional

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class DFS(BaseAlgorithm):
    """A class for Depth First Search algorithm initialised with algorithm parameters."""

    neighbors_quality_order: str
    depth: int
    frontier: queue.LifoQueue[State] = field(default_factory=queue.LifoQueue)

    def __init__(self, neighbors_quality_order: str):
        self.neighbors_quality_order = neighbors_quality_order

    def solve(self, start: State) -> str:
        pass
    """
    Steps of the algorithm:
    1. check if starting state is the target state, if yes return the path to it, else proceed
    2. add starting state to (open-list)frontier
    3. get a list of possible neighbors, reverse the list
    4. iterating over neighbors steps 5 - 6, if all neighbors verified go to step 7
    5. check if neighbor is target state, if yes return path to it, else
    6. add neighbor to open-list(frontier) (without checking existance on list)
    7. add explored state to closed-list(explored), remove from open-list(frontier)
    8. get next state (order like in stack LIFO) from open-list and check if it's in closed-list(explored), if not -> go to step 3
    9. if target state not found -> return None

    :param state: A starting state of the puzzle
    :return: A list of consecutive operations conducted on an initial state to achieve a target state -- a solved puzzle.
    If no solution has been found - return None
    """

    def solve(self, state: State) -> Optional[str]:

        if state.is_target_state():
            return state.get_path_to_state()                        # STEP 1.

        tmp_state: State = state
        # Add the start node to frontier queue, and pop for explore
        DFS.frontier.put_nowait(tmp_state)                          # STEP 2.
        DFS.frontier.get_nowait()

        while not DFS.frontier.empty():

            # Get a list of all neighbors for the current node and reverse order
            neighbors: List[State] = tmp_state.get_neighbors(self.neighbors_quality_order)
            neighbors.reverse()                                     # STEP 3.

            # For each neighbor check if is the target state
            for neighbor in neighbors:                              # STEP 4.
                if neighbor.is_target_state():
                    return neighbor.get_path_to_state()             # STEP 5.
                else:
                    DFS.frontier.put_nowait(neighbor)               # STEP 6.

            # If none of the neighbors is the target:
            # - add the current state to the closed list to avoid revisiting it
            # - remove it from the frontier
            DFS.closed_list[hash(tmp_state)] = tmp_state           # STEP 7.
            DFS.frontier.task_done()      # Jeśli dobrze rozumiem to po ściągnieciu zadania z kolejki, trzeba oznaczyć jako wykonane

        # Get last element from queue and check if it is on closed-list, if not start to explore
        while not DFS.frontier.empty():
            tmp_state = DFS.frontier.get_nowait()                   # STEP 8.
            if hash(tmp_state) not in DFS.closed_list.keys():  # TODO nie wiem czy to dobrze sprawdzam (porównuję) listę z kolejką
                break
            DFS.frontier.task_done()  # Jeśli dobrze rozumiem to po ściągnieciu zadania z kolejki, trzeba oznaczyć jako wykonane

        return None     # TODO tu nie powinno zwracać None? bo jeśli nie znalazło to nie powinno zwrócić ścieżki

    def visualize_solution(self) -> Any:
        pass
