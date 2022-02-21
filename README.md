# Solving a 15 puzzle

## Authors

* Jan Wądołowski
* Bartłomiej Kubiak

## What is a 15 puzzle?

It is a well known puzzle where you have a 4x4 board of tiles with 15 numbers (1...15) and a 0 (or empty) tile. The goal is to arrange the tiles
in ascending order by swapping tiles with an empty tile (only horizontal and diagonal movements are allowed).

## How is the solution achieved?

We used the following algorithms to solve the puzzle:

* Breadth First Search (BFS)
* Depth First Search (DFS)
* A-star (A*)

Moreover, these algorithms can be parametrised. For BFS and DFS user can choose desired searching order and depth limit, whereas, for A* user can choose between Hamming's and Manhattan metrics for calculating distance.
