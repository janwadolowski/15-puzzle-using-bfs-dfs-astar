import queue

from loguru import logger

from algorithms.BaseAlgorithm import BaseAlgorithm
from memory.State import State


class DFS(BaseAlgorithm):
    """A class for Depth First Search algorithm initialised with algorithm parameters."""

    def __init__(self, neighbors_quality_order: str):
        self.neighbors_quality_order = neighbors_quality_order
        self.open_list: queue.LifoQueue[State] = queue.LifoQueue()
        self.closed_list: dict[int, State] = {}
        self.max_depth: int = 0
        self.visited_states: int = 1

    def solve(self, state: State) -> str | None:
        """
        Steps of the algorithm:
        1. check if starting State is the target State, if yes return the path to it, else proceed
        2. add starting State to (open-list)frontier
        3. get a list of possible neighbors, reverse the list
        4. iterating over neighbors steps 5 - 6, if all neighbors verified go to step 7
        5. check if neighbor is target State, if yes return path to it, else
        6. add neighbor to open-list(frontier) (without checking existence on list)
        7. add explored State to closed-list(explored), remove from open-list(frontier)
        8. get next State (order like in stack LIFO) from open-list and check if it's in closed-list(explored), if not -> go to step 3
        9. if target State not found -> return None

        :param state: A starting State of the puzzle
        :return: A list of consecutive operations conducted on an initial array to achieve a target array -- a solved puzzle.
        If no solution has been found - return None
        """
        tmp_state: State | None = None

        # Check if starting State is target State
        if state.is_target_state():
            return state.get_path_to_state()

        # Add the start node to open_list queue, and pop for explore
        self.open_list.put_nowait(state)

        while not self.open_list.empty():
            if tmp_state is None:
                tmp_state = self.open_list.get_nowait()

            # Get a list of all neighbors for the current node and reverse order
            neighbors: list[State] = tmp_state.get_neighbors(
                self.neighbors_quality_order
            )
            neighbors.reverse()

            # Add already explored State to closed_list
            self.closed_list[hash(tmp_state)] = tmp_state

            # For each neighbor check if:
            for neighbor in neighbors:
                self.visited_states += 1
                if self.max_depth < neighbor.get_state_depth():
                    self.max_depth = neighbor.get_state_depth()
                # if neighbor is target State, if true -> return
                if neighbor.is_target_state():
                    logger.info(
                        f"PUZZLE SOLVED - DEPTH={self.max_depth}, path={neighbor.get_path_to_state()}"
                    )
                    return neighbor.get_path_to_state()
                # else: add to open_list without checking its existence on list
                else:
                    self.open_list.put_nowait(neighbor)

            # Set the task on queue as done
            self.open_list.task_done()

            # Get State from queue (LIFO order) and check if it is not on closed_list and depth is less than 20
            # if true start to explore, else get next State and check
            while not self.open_list.empty():
                tmp_state = self.open_list.get_nowait()
                if (
                    hash(tmp_state) not in self.closed_list.keys()
                    and tmp_state.get_state_depth() < 20
                ):
                    break
                self.open_list.task_done()
        logger.info("PUZZLE NOT SOLVED")
        return None
