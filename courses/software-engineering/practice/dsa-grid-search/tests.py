from solution import count_islands, shortest_path


def test_shortest_path_around_walls():
    maze = ["..#", ".##", "..."]
    got = shortest_path(maze, (0, 0), (2, 2))
    assert got == 4, f"expected 4, got {got!r}"


def test_shortest_path_picks_the_shorter_route():
    maze = [
        ".....",
        ".###.",
        ".....",
    ]
    got = shortest_path(maze, (1, 0), (1, 4))
    assert got == 6, f"expected 6, got {got!r}"


def test_unreachable_target_gives_minus_one():
    got = shortest_path([".#.", ".#."], (0, 0), (0, 2))
    assert got == -1, f"expected -1, got {got!r}"


def test_start_equals_end_is_zero_moves():
    got = shortest_path(["..", ".."], (1, 1), (1, 1))
    assert got == 0, f"expected 0, got {got!r}"


def test_count_islands():
    grid = ["11000", "11000", "00100", "00011"]
    got = count_islands(grid)
    assert got == 3, f"expected 3, got {got!r}"
    got = count_islands(["101", "010", "101"])
    assert got == 5, f"diagonals don't connect: expected 5, got {got!r}"


def test_no_land_and_one_huge_island():
    got = count_islands(["000", "000"])
    assert got == 0, f"expected 0, got {got!r}"
    big = ["1" * 200] * 200
    got = count_islands(big)
    assert got == 1, f"expected 1, got {got!r}"
