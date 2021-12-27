import logging
from typing import Any, Dict, List, Literal, Optional, TypeAlias

from loguru import logger

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import TARGET_STATE, State

HEURISTIC_TYPE: TypeAlias = Literal["hamm", "manh"]


class AStar(BaseAlgorithm):
    """A class for A* algorithm initialised with algorithm parameters."""

    def __init__(self, heuristic_type: HEURISTIC_TYPE):
        self.heuristic_type = heuristic_type
        self.open_list: Dict[int, State] = {}
        self.closed_list: Dict[int, State] = {}
        self.max_depth: int = 0
        self.visited_states: int = 1

    """
        Steps of the algorithm:
        1. initialize open-list and closed-list
        2. add first node (starting state) to open-list
        3. start loop until open-list is not empty or solution is found
        4. find the node (state) with the lowest value of f(n) = g(n) + h(n), and pop from open-list
        5. find all possible neighbors, and loop for each: (#7 - #10)
        6. add processed node (state) to closed list
        7. if neighbor is target state -> return
        8. if neighbor is on open-list -> skip
        9. if neighbor is on closed-list -> skip, 
        10. if not on both lists -> calculate f(n) and add to open-list
        11. if target state not found -> return None
        :param state: A starting state of the puzzle
        :return: A list of consecutive operations conducted on an initial state to achieve a target state -- a solved puzzle.
        If no solution has been found - return None
        """

    def solve(self, state: State) -> Optional[str]:

        # Check if starting state is target state
        if state.is_target_state():
            return state.get_path_to_state()

        # Add first state to open_list
        state.heuristic_value = self.calculate_f(state)
        self.open_list[hash(state)] = state

        # Loop until open_list is not empty
        while self.open_list:
            tmp_state: State = None
            tmp_key: int = None
            # Search for the node(state) with the lowest value of f(n), and pop from open-list.
            # if value f(n) is equal in multiple states, take frist occurance from left on the list
            for item in self.open_list.items():
                if tmp_state is None:
                    tmp_key = item[0]
                    tmp_state = item[1]
                elif tmp_state.heuristic_value > item[1].heuristic_value:
                    tmp_key = item[0]
                    tmp_state = item[1]
            self.open_list.pop(tmp_key)

            # Get possible neighbors for state
            neighbors: List[State] = tmp_state.get_neighbors("LRUD")

            # Add tmp_state to closed_list after checking neighbors
            self.closed_list[tmp_key] = tmp_state

            # For each neighbor from list
            for neighbor in neighbors:
                self.visited_states += 1
                if self.max_depth < neighbor.get_state_depth():
                    self.max_depth = neighbor.get_state_depth()

                # Check if neighbor is target state and return if true
                if neighbor.is_target_state():
                    logging.debug(
                        f"PUZZLE SOLVED - DEPTH={self.max_depth}, path={neighbor.get_path_to_state()}"
                    )
                    return neighbor.get_path_to_state()
                # Else: check if exists on open list (skip if true), check if exists on closed list (skip if true)
                # if not on both lists then add to open list
                else:
                    neighbor_hash = hash(neighbor)
                    if neighbor_hash in self.open_list.keys():
                        continue
                    elif neighbor_hash in self.closed_list.keys():
                        continue
                    else:
                        neighbor.heuristic_value = self.calculate_f(neighbor)
                        self.open_list[neighbor_hash] = neighbor

        return None

    def visualize_solution(self) -> Any:
        pass

    def calculate_f(self, state: State) -> int:
        # TODO: test if this works
        """Calculate heuristic: a sum of state's depth and cumulative disorder of its elements."""
        g = state.get_state_depth()
        h = 0

        # Iterate over a State
        for tile in state.state.flat:
            # Count out 0 tile and tiles which are in target positions
            self_tile_coords: tuple[int, int] = state.find_coords(tile)
            target_tile_coords: tuple[int, int] = TARGET_STATE.find_coords(tile)
            if tile != 0 and self_tile_coords != target_tile_coords:
                # If manhattan heuristic calculate distance between tile's current coords, and it's target position
                if self.heuristic_type == "manh":
                    h += State.diff_coords(self_tile_coords, target_tile_coords)
                # If Hamming metric only +1 increment when tile is not in target position
                elif self.heuristic_type == "hamm":
                    h += 1
                # Other heuristics are not implemented
                else:
                    logger.error(f"Unsupported heuristics type: {self.heuristic_type}.")
                    raise NotImplementedError

        return g + h
