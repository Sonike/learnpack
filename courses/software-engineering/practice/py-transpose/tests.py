from solution import transpose


def test_two_by_three():
    got = transpose([[1, 2, 3], [4, 5, 6]])
    want = [[1, 4], [2, 5], [3, 6]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_square_grid():
    got = transpose([[1, 2], [3, 4]])
    want = [[1, 3], [2, 4]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_single_row_becomes_a_column():
    got = transpose([[1, 2, 3]])
    want = [[1], [2], [3]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_and_single_cell():
    assert transpose([]) == [], f"expected [], got {transpose([])!r}"
    assert transpose([[7]]) == [[7]], f"expected [[7]], got {transpose([[7]])!r}"


def test_result_is_lists_and_input_is_unchanged():
    grid = [[1, 2], [3, 4]]
    got = transpose(grid)
    assert grid == [[1, 2], [3, 4]], f"the input was changed to {grid!r}"
    assert all(type(row) is list for row in got), f"each row should be a list, got {got!r}"
