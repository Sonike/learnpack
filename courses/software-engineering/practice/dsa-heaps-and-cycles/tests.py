from solution import has_cycle, top_k_frequent


def test_top_k_most_common_first():
    got = top_k_frequent(["a", "b", "a", "c", "b", "a"], 2)
    assert got == ["a", "b"], f"expected ['a', 'b'], got {got!r}"


def test_top_k_breaks_ties_alphabetically():
    got = top_k_frequent(["dog", "cat", "dog", "cat", "eel"], 2)
    assert got == ["cat", "dog"], f"expected ['cat', 'dog'], got {got!r}"


def test_top_k_larger_than_number_of_words():
    got = top_k_frequent(["x", "y", "x"], 10)
    assert got == ["x", "y"], f"expected ['x', 'y'], got {got!r}"
    got = top_k_frequent([], 3)
    assert got == [], f"expected [], got {got!r}"


def test_acyclic_dependency_graph():
    graph = {"app": ["db", "auth", "logging"], "auth": ["db", "logging"], "db": ["logging"]}
    got = has_cycle(graph)
    assert got is False, f"shared dependencies are not a cycle: expected False, got {got!r}"


def test_finds_cycles():
    cases = [
        {"a": ["b"], "b": ["c"], "c": ["a"]},
        {"a": ["a"]},
        {"x": [], "y": ["z"], "z": ["w"], "w": ["y"]},
    ]
    for graph in cases:
        got = has_cycle(graph)
        assert got is True, f"has_cycle({graph!r}): expected True, got {got!r}"


def test_empty_graph_has_no_cycle():
    got = has_cycle({})
    assert got is False, f"expected False, got {got!r}"
