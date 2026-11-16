from solution import has_duplicate_linear, has_duplicate_quadratic


def test_both_find_a_duplicate():
    for fn in (has_duplicate_quadratic, has_duplicate_linear):
        got = fn(["a", "b", "c", "b"])[0]
        assert got is True, f"{fn.__name__}: expected True, got {got!r}"


def test_both_say_no_when_all_values_differ():
    for fn in (has_duplicate_quadratic, has_duplicate_linear):
        got = fn([5, 3, 9, 1])[0]
        assert got is False, f"{fn.__name__}: expected False, got {got!r}"


def test_step_counts_match_the_example():
    got = has_duplicate_quadratic([3, 1, 4, 1])
    assert got == (True, 5), f"expected {(True, 5)!r}, got {got!r}"
    got = has_duplicate_linear([3, 1, 4, 1])
    assert got == (True, 4), f"expected {(True, 4)!r}, got {got!r}"


def test_empty_list_has_no_duplicates_and_takes_no_steps():
    for fn in (has_duplicate_quadratic, has_duplicate_linear):
        got = fn([])
        assert got == (False, 0), f"{fn.__name__}: expected (False, 0), got {got!r}"


def test_quadratic_steps_grow_about_4x_when_n_doubles():
    small = has_duplicate_quadratic(list(range(100)))[1]
    big = has_duplicate_quadratic(list(range(200)))[1]
    assert small == 4950, f"expected 4950 steps for 100 unique items, got {small!r}"
    assert 3.5 < big / small < 4.5, f"expected about 4x growth, got {big / small:.2f}x"


def test_linear_steps_grow_2x_when_n_doubles():
    small = has_duplicate_linear(list(range(100)))[1]
    big = has_duplicate_linear(list(range(200)))[1]
    assert (small, big) == (100, 200), f"expected (100, 200), got {(small, big)!r}"
