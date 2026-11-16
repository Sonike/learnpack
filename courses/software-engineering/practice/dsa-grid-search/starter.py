from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right


def neighbours(grid: list[str], row: int, col: int):
    """Yield the (row, col) cells next to this one that are inside the grid."""
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            yield r, c


def shortest_path(grid: list[str], start: tuple[int, int], end: tuple[int, int]) -> int:
    """Fewest moves from start to end avoiding '#', or -1. Uses BFS."""
    queue = deque([(start, 0)])
    visited = {start}
    # TODO: while queue: cell, dist = queue.popleft(); if cell == end return dist
    # TODO:   for each neighbour that isn't '#' and isn't visited: mark it, append (neighbour, dist + 1)
    return -1


def count_islands(grid: list[str]) -> int:
    """Number of groups of connected '1' cells. Uses DFS with a stack."""
    visited = set()
    islands = 0
    # TODO: for every (row, col) that is '1' and not visited:
    #         islands += 1; stack = [(row, col)]; mark it visited
    #         while stack: pop a cell; push every '1' neighbour not yet visited (mark it first)
    return islands


if __name__ == "__main__":
    maze = ["..#", ".##", "..."]
    print(shortest_path(maze, (0, 0), (2, 2)))  # want 4
    print(count_islands(["11000", "11000", "00100", "00011"]))  # want 3
