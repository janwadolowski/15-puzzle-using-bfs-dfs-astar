import logging
import queue
from typing import Any, Dict, List, Optional

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class DFS(BaseAlgorithm):
    """A class for Depth First Search algorithm initialised with algorithm parameters."""

    def __init__(self, neighbors_quality_order: str):
        self.neighbors_quality_order = neighbors_quality_order
        self.open_list: queue.LifoQueue[State] = queue.LifoQueue()
        self.closed_list: Dict[int, State] = {}
        self.max_depth: int = 0
        self.visited_states: int = 1

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
        first_run = True

        if state.is_target_state():
            return state.get_path_to_state()  # STEP 1.

        tmp_state: State = state
        # Add the start node to frontier queue, and pop for explore
        self.open_list.put_nowait(tmp_state)  # STEP 2.

        while not self.open_list.empty():
            if first_run:
                tmp_state = self.open_list.get_nowait()
                first_run = False

            # Get a list of all neighbors for the current node and reverse order
            neighbors: List[State] = tmp_state.get_neighbors(
                self.neighbors_quality_order
            )
            neighbors.reverse()  # STEP 3.

            self.closed_list[hash(tmp_state)] = tmp_state  # STEP 7.

            # For each neighbor check if is the target state
            for neighbor in neighbors:  # STEP 4.
                self.visited_states += 1
                if self.max_depth < neighbor.get_state_depth():
                    self.max_depth = neighbor.get_state_depth()
                if neighbor.is_target_state():
                    logging.debug(f"PUZZLE SOLVED - DEPTH={self.max_depth}, path={neighbor.get_path_to_state()}")
                    return neighbor.get_path_to_state()  # STEP 5.
                else:
                    self.open_list.put_nowait(neighbor)  # STEP 6.

            # If none of the neighbors is the target - add the current state to the closed list to avoid revisiting it

            self.open_list.task_done()

            # Get last element from queue and check if it is on closed-list, if not start to explore
            while not self.open_list.empty():
                tmp_state = self.open_list.get_nowait()  # STEP 8.
                if hash(tmp_state) not in self.closed_list.keys() and tmp_state.get_state_depth() < 20:
                    break
                #logging.debug(f"STATE ON CLOSED-LIST -> CONTINUE")
                self.open_list.task_done()
        logging.debug("PUZZLE NOT SOLVED")
        return None  # STEP 9.

    def visualize_solution(self) -> Any:
        pass
