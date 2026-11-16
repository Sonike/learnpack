from solution import safe_divide_all


def test_all_good_pairs():
    got = safe_divide_all([(10, 2), (9, 3), (1, 4)])
    want = ([5.0, 3.0, 0.25], [])
    assert got == want, f"expected {want!r}, got {got!r}"


def test_division_by_zero_is_reported_with_its_index():
    got = safe_divide_all([(10, 2), (1, 0), (9, 3)])
    want = ([5.0, 3.0], ["pair 1: division by zero"])
    assert got == want, f"expected {want!r}, got {got!r}"


def test_wrong_types_are_reported_too():
    results, errors = safe_divide_all([("6", 2)])
    assert results == [], f"expected no results, got {results!r}"
    want = ["pair 0: unsupported operand type(s) for /: 'str' and 'int'"]
    assert errors == want, f"expected {want!r}, got {errors!r}"


def test_empty_input_gives_two_empty_lists():
    got = safe_divide_all([])
    assert got == ([], []), f"expected ([], []), got {got!r}"


def test_other_bugs_still_crash():
    try:
        safe_divide_all([(1, 2, 3)])  # three values can't unpack into (a, b)
    except ValueError:
        return
    assert False, "only ZeroDivisionError and TypeError should be caught; a ValueError must still crash"
