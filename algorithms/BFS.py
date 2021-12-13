import copy
from abc import ABC
from typing import Any, List

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class BFS(BaseAlgorithm, ABC):
    """A container class for methods and variables connected with Breadth First Search algorithm. Not meant to be instantiated."""

    @staticmethod
    def solve(state: State) -> List[State.DIRECTIONS_ENUM]:
        # TODO: verify
        """
        Steps of the algorithm:
        1. check if a state is the target state, if yes return the path to it, else proceed
        2. check if a state is in the closed list, if yes skip it, else proceed
        3. add state to frontier
        4. get a list of possible neighbors
        5. iterating over neighbors list do steps 1 -4
        6. if all neighbors have been visited add the state to the closed list

        :param state: A starting state of the puzzle
        :return: A list of consecutive operations conducted on an initial state to achieve a target state -- a solved puzzle
        """
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

    @staticmethod
    def visualize_solution() -> Any:
        pass
