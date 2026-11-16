from solution import rotate


def test_rotates_right():
    got = rotate([1, 2, 3, 4, 5], 2)
    assert got == [4, 5, 1, 2, 3], f"expected [4, 5, 1, 2, 3], got {got!r}"


def test_k_larger_than_the_list_wraps_around():
    got = rotate([1, 2, 3, 4, 5], 7)
    assert got == [4, 5, 1, 2, 3], f"expected [4, 5, 1, 2, 3], got {got!r}"


def test_negative_k_rotates_left():
    got = rotate(["a", "b", "c"], -1)
    assert got == ["b", "c", "a"], f"expected ['b', 'c', 'a'], got {got!r}"


def test_zero_and_full_rotation_give_the_same_items():
    for k in [0, 3, 6]:
        got = rotate(["a", "b", "c"], k)
        assert got == ["a", "b", "c"], f"rotate(['a', 'b', 'c'], {k}): expected ['a', 'b', 'c'], got {got!r}"


def test_empty_list():
    got = rotate([], 3)
    assert got == [], f"expected [], got {got!r}"


def test_input_is_not_changed_and_result_is_a_new_list():
    original = [1, 2, 3, 4, 5]
    got = rotate(original, 0)
    assert original == [1, 2, 3, 4, 5], f"the input was changed to {original!r}"
    assert got is not original, "return a new list, not the same list object"
    rotate(original, 2)
    assert original == [1, 2, 3, 4, 5], f"the input was changed to {original!r}"
