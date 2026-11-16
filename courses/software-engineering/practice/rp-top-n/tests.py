from solution import top_n


def test_returns_the_most_common_first():
    got = top_n(["cat", "dog", "cat", "bird", "cat", "dog"], 2)
    want = [("cat", 3), ("dog", 2)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_counts_case_insensitively():
    got = top_n(["The", "the", "THE", "end"], 1)
    want = [("the", 3)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ties_keep_first_seen_order():
    got = top_n(["b", "a", "c", "a", "b"], 3)
    want = [("b", 2), ("a", 2), ("c", 1)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_n_bigger_than_the_vocabulary_returns_everything():
    got = top_n(["a", "b"], 10)
    want = [("a", 1), ("b", 1)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_zero_or_negative_n_and_empty_words():
    assert top_n(["a", "a"], 0) == [], f"n=0: expected [], got {top_n(['a', 'a'], 0)!r}"
    assert top_n(["a"], -1) == [], f"n=-1: expected [], got {top_n(['a'], -1)!r}"
    got = top_n(["", "x", ""], 5)
    assert got == [("x", 1)], f"empty strings should be ignored, got {got!r}"
