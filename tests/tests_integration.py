import argparse

import pytest

from algorithms.DFS import DFS


class TestIntegration:
    @pytest.fixture
    def cli_parser(self):
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
        yield parser

    def initialize_dfs(self, cli_parser):
        dfs = DFS(cli_parser.)

        parsed = parser.(['Strategy', 'dfs'])
        yield example_state

    parser = argparse.ArgumentParser()

    parsed = parser.parse_args(['Strategy', 'dfs'])


dfs
RDUL
4
x4_01_00001.txt
4
x4_01_00001_dfs_rdul_sol.txt
4
x4_01_00001_dfs_rdul_stats.txt
