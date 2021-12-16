import argparse
import os


def main() -> None:
    # Program arguments
    # Example: python program.py bfs RDUL 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt
    parser = argparse.ArgumentParser()
    parser.add_argument("Strategy", type=str, help="Algorithm [bfs, dfs, astr]")
    parser.add_argument("Strategy_param", type=str, help="Algorithm [bfs&dfs: permutations of [L,R,U,D]; astr: hamm/manh]")
    parser.add_argument("Input_file", type=str, help="Input puzzle .txt file")
    parser.add_argument("Output_Solution", type=str, help="Output .txt file name with puzzle solution steps")
    parser.add_argument("Output_Stats", type=str, help="Output .txt file with algorithm statistics")
    args = parser.parse_args()

    # Output files
    solution_file = prepare_file("./" + args.Output_Solution)
    stats_file = prepare_file("./" + args.Output_Stats)

    if args.Strategy == 'bfs':
        print("Start BFS ")
        moves = "LRDULDR"  # Moves made to solve the puzzle # TODO ??? do sprawdzenia co będzie zwracać algorytm
        write_to_solution_file(moves, len(moves), solution_file)  # TODO Dodać parametr
        write_to_stats_file(len(moves), 1, 2, 3, 124.23001, stats_file)  # TODO Uzupełnic parametry

    elif args.Strategy == 'dfs':
        print("Start DFS")
        moves = "LRDULDR"  # Moves made to solve the puzzle # TODO ??? do sprawdzenia co będzie zwracać algorytm
        write_to_solution_file(moves, len(moves), solution_file)  # TODO Dodać parametr
        write_to_stats_file(len(moves), 1, 2, 3, 124.23001, stats_file)  # TODO  Uzupełnic parametry

    elif args.Strategy == 'astr':
        print("Start A*")
        moves = "LRDULDR"  # Moves made to solve the puzzle  # TODO ??? do sprawdzenia co będzie zwracać algorytm
        write_to_solution_file(moves, len(moves), solution_file)  # TODO Dodać parametr
        write_to_stats_file(len(moves), 1, 2, 3, 124.23001, stats_file)  # TODO Uzupełnic parametry

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
    if n_moves == -1:
        sol_file.write(str(n_moves))
    else:
        sol_file.write(str(n_moves) + "\n" + moves)


def write_to_stats_file(n_moves: int, frontier: int, explored: int, recursion: int, time_elapsed: float,
                        stats_file) -> None:
    stats_file.write(str(n_moves) + "\n" +
                     str(frontier) + "\n" +
                     str(explored) + "\n" +
                     str(recursion) + "\n" +
                     str(format(time_elapsed, '.3f')) + "\n")


if __name__ == "__main__":
    main()
