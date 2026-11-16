# Searching a grid: BFS and DFS

A grid is a list of equal-length strings. Cell `(row, col)` is `grid[row][col]`. From a cell you may move **up, down, left or right** (no diagonals) and never off the edge.

## 1. Shortest path with BFS

```python
def shortest_path(grid: list[str], start: tuple[int, int], end: tuple[int, int]) -> int: ...
```

- `.` is open floor, `#` is a wall. `start` and `end` are `(row, col)` cells that are not walls.
- Return the **fewest moves** to get from `start` to `end`, or `-1` if you can't reach it. If `start == end`, return `0`.
- Use **breadth-first search** with `collections.deque`: put `(start, 0)` in the queue and `start` in a `visited` set. Repeatedly `popleft` a cell; for each open, unvisited neighbour, mark it visited and append it with `distance + 1`. BFS reaches cells in order of distance, so the first time you reach `end` is the shortest way.

```python
maze = [
    "..#",
    ".##",
    "...",
]
shortest_path(maze, (0, 0), (2, 2))  # 4   down, down, right, right
shortest_path([".#.", ".#."], (0, 0), (0, 2))  # -1  the wall splits the grid
```

## 2. Count islands with DFS

```python
def count_islands(grid: list[str]) -> int: ...
```

- `1` is land, `0` is water. An **island** is a group of land cells connected up, down, left or right.
- Return how many islands there are.
- Scan every cell. When you find land you haven't visited, that's a new island: count it, then use **depth-first search** to visit every land cell connected to it. Use a list as a stack (`append` / `pop`) rather than recursion, so a huge island can't hit Python's recursion limit.

```python
count_islands([
    "11000",
    "11000",
    "00100",
    "00011",
])  # 3
```
