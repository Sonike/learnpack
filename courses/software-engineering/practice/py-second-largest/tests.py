from solution import second_largest


def test_mixed_numbers():
    got = second_largest([3, 9, 4, 1])
    assert got == 4, f"expected 4, got {got!r}"


def test_duplicates_of_the_largest_are_skipped():
    got = second_largest([3, 9, 4, 9, 1])
    assert got == 4, f"expected 4, got {got!r}"


def test_negative_numbers():
    got = second_largest([-2, -8, -5])
    assert got == -5, f"expected -5, got {got!r}"


def test_no_second_value_gives_none():
    for nums in [[], [42], [7, 7, 7]]:
        got = second_largest(nums)
        assert got is None, f"second_largest({nums!r}): expected None, got {got!r}"


def test_input_list_is_not_changed():
    nums = [5, 1, 5, 3]
    second_largest(nums)
    assert nums == [5, 1, 5, 3], f"the input list was changed to {nums!r}"
