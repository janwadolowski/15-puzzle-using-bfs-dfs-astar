import copy
from typing import Any, List, Optional

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class DFS(BaseAlgorithm):
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

    def solve(self, state: State) -> Optional[List[State.DIRECTIONS_ENUM]]:

        if state.is_target_state():
            return state.get_path_to_state()                        # STEP 1.

        tmp_state: State = state
        # Add the start node to frontier
        DFS.frontier.append(tmp_state)                              # STEP 2.

        while DFS.frontier:
            # Get a list of all neighbors for the current node and reverse order
            neighbors: List[State] = tmp_state.get_neighbors()      # STEP 3.
            neighbors.reverse()

            # For each neighbor check if is the target state
            for neighbor in neighbors:                              # STEP 4.
                if neighbor.is_target_state():
                    return neighbor.get_path_to_state()             # STEP 5.
                else:
                    DFS.frontier.append(neighbor)                   # STEP 6.

            # If none of the neighbors is the target:
            # - add the current state to the closed list to avoid revisiting it
            # - remove it from the frontier
            DFS.closed_list.add(copy.deepcopy(tmp_state))           # STEP 7.
            DFS.frontier.remove(tmp_state)

            # Get last element on the list and check if it is on closed-list, if not start to explore
            while True:
                tmp_state = DFS.frontier[len(DFS.frontier) - 1]     # STEP 8.
                if tmp_state not in DFS.closed_list:            # TODO nie wiem czy to dobrze sprawdzam (porównuję) listę z kolejką
                    break
                DFS.frontier.remove(tmp_state)

        return tmp_state.get_path_to_state()     # TODO tu nie powinno zwracać None? bo jeśli nie znalazło to nie powinno zwrócić ścieżki

    def visualize_solution(self) -> Any:
        pass

    depth: int
