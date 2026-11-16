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
    while queue:
        cell, dist = queue.popleft()
        if cell == end:
            return dist
        for r, c in neighbours(grid, *cell):
            if grid[r][c] != "#" and (r, c) not in visited:
                visited.add((r, c))
                queue.append(((r, c), dist + 1))
    return -1


def count_islands(grid: list[str]) -> int:
    """Number of groups of connected '1' cells. Uses DFS with a stack."""
    visited = set()
    islands = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != "1" or (row, col) in visited:
                continue
            islands += 1
            visited.add((row, col))
            stack = [(row, col)]
            while stack:
                for r, c in neighbours(grid, *stack.pop()):
                    if grid[r][c] == "1" and (r, c) not in visited:
                        visited.add((r, c))
                        stack.append((r, c))
    return islands
