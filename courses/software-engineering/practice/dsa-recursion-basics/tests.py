from solution import count_paths, flatten, power


def test_flatten_nested_lists():
    got = flatten([1, [2, [3, 4]], [], 5])
    assert got == [1, 2, 3, 4, 5], f"expected [1, 2, 3, 4, 5], got {got!r}"


def test_flatten_keeps_strings_whole_and_handles_empty():
    got = flatten([["a", ["bc"]], [[[]]], "d"])
    assert got == ["a", "bc", "d"], f"expected ['a', 'bc', 'd'], got {got!r}"
    got = flatten([])
    assert got == [], f"expected [], got {got!r}"


def test_power_small_cases():
    for base, exp in [(2, 10), (5, 0), (3, 1), (-2, 3), (7, 13)]:
        got = power(base, exp)
        assert got == base**exp, f"power({base}, {exp}): expected {base**exp}, got {got!r}"


def test_power_halves_the_exponent():
    got = power(2, 5000)
    assert got == 2**5000, "power(2, 5000) gave the wrong number"


def test_count_paths():
    for rows, cols, want in [(2, 2, 2), (3, 3, 6), (1, 7, 1), (3, 7, 28), (5, 5, 70)]:
        got = count_paths(rows, cols)
        assert got == want, f"count_paths({rows}, {cols}): expected {want}, got {got!r}"


def test_one_by_one_grid_has_one_path():
    got = count_paths(1, 1)
    assert got == 1, f"expected 1, got {got!r}"
