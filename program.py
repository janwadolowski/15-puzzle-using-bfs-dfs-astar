import argparse
import datetime
import os

from algorithms.AStar import AStar
from algorithms.BFS import BFS
from algorithms.DFS import DFS
from memory.State import State


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
        bfs = BFS
        solve_puzzle(bfs, input_file_path, solution_file, stats_file)

    elif args.Strategy == "dfs":
        print("Start DFS")
        dfs = DFS
        solve_puzzle(dfs, input_file_path, solution_file, stats_file)

    elif args.Strategy == "astr":
        print("Start A*")
        astr = AStar
        solve_puzzle(astr, input_file_path, solution_file, stats_file)

    solution_file.close()
    stats_file.close()


# Not necessary, because output files needs to be in the same directory as input files
def ensure_dir(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def prepare_file(file_path: str):
    file_dir = os.path.realpath(file_path)
    # ensure_dir(file_dir)
    file = open(file_dir, "w+")
    return file


def write_to_solution_file(moves: str, n_moves: int, sol_file) -> None:
    # TODO how to check condition if puzzle was solved or not
    if n_moves == -1:
        sol_file.write(str(n_moves))
    else:
        sol_file.write(str(n_moves) + "\n" + moves)


def write_to_stats_file(
    n_moves: int,
    frontier: int,
    explored: int,
    recursion: int,
    time_elapsed: float,
    stats_file,
) -> None:
    stats_file.write(
        str(n_moves)
        + "\n"
        + str(frontier)
        + "\n"
        + str(explored)
        + "\n"
        + str(recursion)
        + "\n"
        + str(format(time_elapsed, ".3f"))
        + "\n"
    )


def solve_puzzle(algorithm, input_file_path, output_solution, output_stats):
    # Start time marker
    start_time = datetime.datetime.now()
    # Run algorithm to solve the puzzle
    moves = algorithm.solve(State.load_state(input_file_path))
    # End time marker
    end_time = datetime.datetime.now()
    # Time difference between markers in milliseconds
    time_in_ms = (end_time - start_time).total_seconds() * 1000.0

    # TODO Change path from list to string
    write_to_solution_file(moves, len(moves), output_solution)
    # TODO Uzupełnic parametr głębokość rekursji
    write_to_stats_file(
        len(moves),
        len(algorithm.frontier),
        len(algorithm.closed_list),
        3,
        time_in_ms,
        output_stats,
    )


if __name__ == "__main__":
    main()
