import copy
from typing import Any, List, Optional

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class BFS(BaseAlgorithm):
    """A class for Breadth First Search algorithm initialised with an algorithm parameter."""

    neighbors_quality_order: str

    def solve(self, state: State) -> Optional[str]:
        # TODO: verify
        """
        Steps of the algorithm:
        1. check if a state is the target state, if yes return, no moves need to be taken as the initial state is the target state, else:
        2. check if a state is in the closed list, if yes skip it, else proceed
        3. add state to frontier
        4. get a list of possible neighbors
        5. iterating over neighbors list do steps 1 -4
        6. if all neighbors have been visited add the state to the closed list

        :param state: A starting state of the puzzle
        :return: A list of consecutive operations conducted on an initial state to achieve a target state -- a solved puzzle.
                 If no solution has been found - return None
        """
        # if initial state is the target state we don't even enter the loop
        if state.is_target_state():
            return state.get_path_to_state()

        tmp_state: State = state
        while not tmp_state.is_target_state():
            # Add the current node to frontier
            BFS.frontier.append(tmp_state)
            # Get a list of all neighbors for the current node
            neighbors: List[State] = tmp_state.get_neighbors()
            # Sift out already visited neighbors
            neighbors = list(filter(lambda x: x not in BFS.closed_list, neighbors))
            # Add neighbors to the frontier list
            BFS.frontier.extend(neighbors)
            # For each neighbor check if it's the target state
            for neighbor in neighbors:
                if neighbor.is_target_state():
                    return neighbor.get_path_to_state()

            # If none of the neighbors is the target:
            # - add the current state to the closed list to avoid revisiting it
            # - remove it from the frontier
            BFS.closed_list.add(copy.deepcopy(tmp_state))
            BFS.frontier.remove(tmp_state)
            tmp_state = BFS.frontier[0]
        return tmp_state.get_path_to_state()

    def visualize_solution(self) -> Any:
        # TODO: implement (maybe)
        pass
