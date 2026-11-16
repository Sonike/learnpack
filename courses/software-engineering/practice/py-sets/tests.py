from solution import common_friends, unique_in_order


def test_common_friends_sorted():
    got = common_friends({"ana", "ben", "cy"}, {"cy", "dee", "ana"})
    assert got == ["ana", "cy"], f"expected ['ana', 'cy'], got {got!r}"


def test_no_common_friends():
    got = common_friends({"ana"}, {"ben"})
    assert got == [], f"expected [], got {got!r}"
    got = common_friends(set(), {"ben"})
    assert got == [], f"expected [] with an empty set, got {got!r}"


def test_unique_keeps_first_occurrences_in_order():
    got = unique_in_order([3, 1, 3, 2, 1])
    assert got == [3, 1, 2], f"expected [3, 1, 2], got {got!r}"


def test_unique_with_strings_and_no_duplicates():
    assert unique_in_order(["b", "a", "b"]) == ["b", "a"], f"got {unique_in_order(['b', 'a', 'b'])!r}"
    assert unique_in_order(["x", "y"]) == ["x", "y"], f"got {unique_in_order(['x', 'y'])!r}"


def test_unique_of_empty_list_and_input_unchanged():
    assert unique_in_order([]) == [], f"expected [], got {unique_in_order([])!r}"
    items = [1, 1, 2]
    unique_in_order(items)
    assert items == [1, 1, 2], f"the input was changed to {items!r}"
