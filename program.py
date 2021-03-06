import argparse
import datetime
import os
import sys
from pathlib import Path
from typing.io import TextIO

from loguru import logger

from algorithms.AStar import AStar
from algorithms.BFS import BFS
from algorithms.DFS import DFS
from memory.State import State

# Write logs from program execution to a file
logger.add(
    Path("logs/program_exec_info.log"),
    retention="1 day",
    format="{elapsed} {level} {line}: {module}.{function}: {message}",
    level="INFO",
)
# And show error logs in STDERR
logger.add(sys.stderr, format="{elapsed} {level} {function} {message}", level="ERROR")
logger.remove(0)  # remove the default DEBUG logger


def main() -> None:
    # Program arguments
    # Example: python program.py bfs RDUL 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt
    parser = argparse.ArgumentParser()
    parser.add_argument("Strategy", type=str, help="Algorithm [bfs, dfs, astr]")
    parser.add_argument(
        "Strategy_param",
        type=str,
        help="For bfs or dfs: any permutation of: LRUD; For astr: hamm | manh",
    )
    parser.add_argument("Input_file", type=str, help="Input puzzle .txt file")
    parser.add_argument(
        "Output_Solution",
        type=str,
        help="Output .txt file name with puzzle solution steps",
    )
    parser.add_argument(
        "Output_Stats", type=str, help="Output .txt file with algorithm statistics"
    )
    args = parser.parse_args()

    # Output files
    solution_file = prepare_file("./" + args.Output_Solution)
    stats_file = prepare_file("./" + args.Output_Stats)

    # Input file path
    input_file_path = os.path.realpath("./" + args.Input_file)

    if args.Strategy == "bfs":
        bfs = BFS(args.Strategy_param)
        solve_puzzle(bfs, input_file_path, solution_file, stats_file)

    elif args.Strategy == "dfs":
        dfs = DFS(args.Strategy_param)
        solve_puzzle(dfs, input_file_path, solution_file, stats_file)

    elif args.Strategy == "astr":
        astr = AStar(args.Strategy_param)
        solve_puzzle(astr, input_file_path, solution_file, stats_file)

    solution_file.close()
    stats_file.close()


def prepare_file(file_path: str) -> TextIO:
    """Creates a file under a specified path."""
    file_dir = os.path.realpath(file_path)
    return open(file_dir, "w+")


def write_to_solution_file(moves: str, sol_file) -> None:
    if moves is None:  # If the result was not found we write -1
        sol_file.write(str(-1))
    else:  # else write length and path to the target state
        sol_file.write(f"{len(moves)}\n{moves}")


def write_to_stats_file(
    n_moves: int,
    visited: int,
    explored: int,
    recursion: int,
    time_elapsed: float,
    stats_file,
) -> None:
    stats_file.write(
        f"{n_moves}\n{visited}\n{explored}\n{recursion}\n{format(time_elapsed, '.3f')}\n"
    )


def solve_puzzle(algorithm, input_file_path, output_solution, output_stats):
    state = State.load_state(input_file_path)
    # Start time marker
    start_time = datetime.datetime.now()
    # Run algorithm to solve the puzzle
    moves = algorithm.solve(state)
    # End time marker
    end_time = datetime.datetime.now()
    # Time difference between markers in milliseconds
    time_in_ms = (end_time - start_time).total_seconds() * 1000.0

    write_to_solution_file(moves, output_solution)
    n_moves = -1
    if moves is not None:
        n_moves = len(moves)

    write_to_stats_file(
        n_moves,
        algorithm.visited_states,
        len(algorithm.closed_list),
        algorithm.max_depth,
        time_in_ms,
        output_stats,
    )


if __name__ == "__main__":
    main()
