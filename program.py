import argparse
import datetime
import logging
import os
import sys

from loguru import logger

from algorithms.AStar import AStar
from algorithms.BFS import BFS
from algorithms.DFS import DFS
from memory.State import State

logging.basicConfig(level=logging.DEBUG)
# Write logs from program execution to a file
logger.add(open(f"log_{datetime.datetime.now()}.txt", "w+"), format="[{elapsed}] {level} {line}: {module}.{function}: {message}", level="INFO")
# And show error logs in terminal
logger.add(sys.stderr, format="{elapsed} {level} {function} {message}", level="ERROR")


def main() -> None:
    # Program arguments
    # Example: python program.py bfs RDUL 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt
    parser = argparse.ArgumentParser()
    parser.add_argument("Strategy", type=str, help="Algorithm [bfs, dfs, astr]")
    parser.add_argument(
        "Strategy_param",
        type=str,
        help="Algorithm [bfs&dfs: permutations of [L,R,U,D]; astr: hamm/manh]",
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
        print("Start BFS")
        bfs = BFS(args.Strategy_param)
        solve_puzzle(bfs, input_file_path, solution_file, stats_file)

    elif args.Strategy == "dfs":
        dfs = DFS(args.Strategy_param)
        solve_puzzle(dfs, input_file_path, solution_file, stats_file)

    elif args.Strategy == "astr":
        print("Start A*")
        astr = AStar(args.Strategy_param)
        solve_puzzle(astr, input_file_path, solution_file, stats_file)

    solution_file.close()
    stats_file.close()


def prepare_file(file_path: str):
    file_dir = os.path.realpath(file_path)
    file = open(file_dir, "w+")
    return file


def write_to_solution_file(moves: str, sol_file) -> None:
    # TODO how to check condition if puzzle was solved or not
    if moves is None:
        sol_file.write(str(-1))
    else:
        sol_file.write(f"{len(moves)}\n{moves}")


def write_to_stats_file(
    n_moves: int,
    frontier: int,
    explored: int,
    recursion: int,
    time_elapsed: float,
    stats_file,
) -> None:
    stats_file.write(
        f"{n_moves}\n{frontier}\n{explored}\n{recursion}\n{format(time_elapsed, '.3f')}\n"
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
    # TODO Uzupełnic parametr głębokość rekursji
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
