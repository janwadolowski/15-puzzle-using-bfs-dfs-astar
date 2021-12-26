import logging
from typing import Any, List, Dict, Optional

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class AStar(BaseAlgorithm):
    """A class for A* algorithm initialised with algorithm parameters."""
    def __init__(self, heuristic_type: str):
        self.heuristic_type = heuristic_type
        self.open_list: List[State] = []
        self.closed_list: Dict[int, State] = {}
        self.max_depth: int = 0
        self.visited_states: int = 1

    """
        Steps of the algorithm:
        1. initialize open-list and closed-list
        2. add first node (starting state) to open-list
        3. start loop until open-list is not empty or solution is found
        4. find the node (state) with the lowest value of f(n) = g(n) + h(n), and pop from open-list
        5. find all possible neighbors, and loop for each: (#6 - #8)
        6. if neighbor is target state -> return, else calculate f(n)
        7. if neighbor is on open-list with lower f(n) value -> skip, else -> Step #8
        8. if neighbor is on closed-list with lower f(n) value -> skip, else -> add to open-list
        9. add processed node (state) to closed list
        10. if target state not found -> return None

        :param state: A starting state of the puzzle
        :return: A list of consecutive operations conducted on an initial state to achieve a target state -- a solved puzzle.
        If no solution has been found - return None
        """

    def solve(self, state: State) -> Optional[str]:

        if state.is_target_state():
            return state.get_path_to_state()

        self.open_list.append(state)

        while not self.open_list.empty():
            tmp_state: State = None
            # search for the node(state) with the lowest value of f(n), and remove from open-list
            for st in self.open_list:
                if tmp_state is None:
                    tmp_state = st
                elif self.calculateF(tmp_state, self.heuristic_type) > self.calculateF(st, self.heuristic_type):
                    tmp_state = st
            self.open_list.remove(tmp_state)

            neighbors: List[State] = tmp_state.get_neighbors("LRUD")

            for neighbor in neighbors:
                self.visited_states += 1
                if self.max_depth < neighbor.get_state_depth():
                    self.max_depth = neighbor.get_state_depth()
                if neighbor.is_target_state():
                    logging.debug(f"PUZZLE SOLVED - DEPTH={self.max_depth}, path={neighbor.get_path_to_state()}")
                    return neighbor.get_path_to_state()
                else:
                    f_neighbor = self.calculateF(neighbor, self.heuristic_type)
                    if True: # TODO sprawdzić czy neighbor jest na open-list, jeśli tak i ma mniejszą wartość f(n) niż neighbor to skip
                        pass
                    else: # TODO sprawdzić czy neighbor jest na close-list, jeśli tak i ma mniejszą wartość f(n) niż neighbor to skip, inczej add to open-list
                        pass

            self.closed_list[hash(tmp_state)] = tmp_state

        return None

    def visualize_solution(self) -> Any:
        pass

    def calculateF(self, state: State, heuristic: str) -> [int]:
        g = state.get_state_depth()
        h = 0
        if heuristic == 'hamm':
            pass  # TODO napisać obliczenia heurystyki dla danej metryki
        elif heuristic == 'manh':
            pass

        return g + h


