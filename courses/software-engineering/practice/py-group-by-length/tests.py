from solution import group_by_length


def test_groups_words_by_length():
    got = group_by_length(["hi", "cat", "a", "dog", "ok"])
    want = {2: ["hi", "ok"], 3: ["cat", "dog"], 1: ["a"]}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_keeps_input_order_inside_each_group():
    got = group_by_length(["dog", "cat", "ant"])
    assert got == {3: ["dog", "cat", "ant"]}, f"expected {{3: ['dog', 'cat', 'ant']}}, got {got!r}"


def test_keys_in_order_first_seen():
    got = list(group_by_length(["three", "a", "to", "four"]))
    assert got == [5, 1, 2, 4], f"expected keys [5, 1, 2, 4], got {got!r}"


def test_keeps_duplicates():
    got = group_by_length(["yes", "yes", "no"])
    want = {3: ["yes", "yes"], 2: ["no"]}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_list_and_empty_string():
    assert group_by_length([]) == {}, f"expected {{}}, got {group_by_length([])!r}"
    got = group_by_length([""])
    assert got == {0: [""]}, f"expected {{0: ['']}}, got {got!r}"
