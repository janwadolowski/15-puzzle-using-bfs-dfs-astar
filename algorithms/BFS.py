import logging
from collections import deque
from typing import Deque, Dict, Optional

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class BFS(BaseAlgorithm):
    """A class for Breadth First Search algorithm initialised with an algorithm parameter."""

    def __init__(
        self,
        neighbors_quality_order: str,
    ):
        self.visited_states = 0
        self.max_depth = 0
        self.closed_list: Dict[int, State] = {}  # mapping {hash(State): State}
        self.neighbors_query_order = neighbors_quality_order
        self.frontier: Deque[State] = deque()

    def solve(self, state: State) -> Optional[str]:
        """
        Steps of the algorithm:
        1. check if a State is the target array, if yes return, no moves need to be taken as the initial State is the target State, else:
        2. check if a State is in the closed list, if yes skip it, else proceed
        3. add a State to frontier
        4. get a list of possible neighbors
        5. iterating over neighbors list do steps 1 -4
        6. if all neighbors have been visited add the State to the closed list

        :param state: An initial State of the puzzle
        :return: A list of consecutive operations conducted on an initial State to achieve a target State -- a solved puzzle.
                 If no solution has been found - return None
        """
        # if initial State is the target State we don't even enter the loop
        if state.is_target_state():
            logging.info("Initial state is target state. Returning [].")
            return state.get_path_to_state()
        else:
            self.frontier.append(state)
            logging.debug(f"Added initial state to the frontier:\n{str(state)}.")

            while self.frontier:  # == while not empty (empty deque is a falsy value)
                logging.debug(f"Frontier not empty, {len(self.frontier)} elements.")

                examined_state = self.frontier.popleft()
                logging.debug(
                    f"Popped first element from the deque:\n{str(examined_state)}"
                )

                self.closed_list[hash(examined_state)] = examined_state
                logging.debug(
                    f"Added examined_state to the closed_list:\n{hash(examined_state)}: {str(examined_state)}"
                )

                logging.debug(
                    f"State examined. Fetching neighbors:\n{examined_state.get_neighbors(self.neighbors_query_order)}"
                )
                for neighbor in examined_state.get_neighbors(
                    self.neighbors_query_order
                ):
                    logging.debug(f"Checking a neighbor:\n{str(neighbor)}")

                    if neighbor.is_target_state():
                        path = neighbor.get_path_to_state()
                        logging.info(f"Found target state, returning path: {path}")
                        return path
                    elif (
                        neighbor in self.frontier or hash(neighbor) in self.closed_list
                    ):
                        logging.debug(f"Neighbor in open or closed list: {neighbor}")
                        continue  # do nothing with it

                    else:
                        self.frontier.append(neighbor)
