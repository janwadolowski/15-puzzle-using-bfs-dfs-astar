import os
import re
import sys
from itertools import permutations
from pathlib import Path, PurePath

import pytest
from loguru import logger

PUZZLES_DIRECTORY = Path(r"D:\MEGAsync\Studia\SISE\input_puzzles")
logger.add(sys.stderr, format="{elapsed} {level} {function} {message}", level="DEBUG")


def _absolute_file_paths(directory: PurePath, depth: int | None = None) -> list[str]:
    """Create a list of absolute filepaths for files in a given directory."""
    paths: list[str] = []
    regex = rf"^\dx\d_*0{depth}_\d+.txt"
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            # append a filepath if filename matches a depth level or if depth is not specified
            if depth is None or re.search(regex, f):
                paths.append(os.path.abspath(os.path.join(dirpath, f)))
    return paths


input_puzzle_files = _absolute_file_paths(PUZZLES_DIRECTORY)
query_order_permutations = permutations("LRUD", 4)
parameters = [
    ("astar", ("hamm", "manh"), input_puzzle_files),
    ("bfs", query_order_permutations, input_puzzle_files),
    ("dfs", query_order_permutations, input_puzzle_files),
]


@pytest.mark.parametrize("algorithm, algo_parameter", parameters)
def test_integration(
    algorithm,
    algo_parameter,
    puzzle_file,
    expected_output,
):
    script = open(Path("../program.py"))
    code = script.read()
    # set the arguments to be read by script.py
    sys.argv = [
        algorithm,
        algo_parameter,
        puzzle_file,
        expected_output,
    ]
