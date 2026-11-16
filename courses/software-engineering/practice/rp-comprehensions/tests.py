from solution import flatten, initials, squares_of_evens, word_lengths


def test_squares_of_evens():
    got = squares_of_evens([1, 2, 3, 4, -6])
    want = [4, 16, 36]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_word_lengths():
    got = word_lengths(["hi", "there", ""])
    want = {"hi": 2, "there": 5, "": 0}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_initials_are_unique_upper_case_letters():
    got = initials(["ada", "Alan", "grace", "", "Guido"])
    want = {"A", "G"}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_flatten_keeps_order_and_skips_empty_rows():
    got = flatten([[1, 2], [], [3], [4, 5]])
    want = [1, 2, 3, 4, 5]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_inputs():
    got = (squares_of_evens([]), word_lengths([]), initials([]), flatten([]))
    want = ([], {}, set(), [])
    assert got == want, f"expected {want!r}, got {got!r}"
