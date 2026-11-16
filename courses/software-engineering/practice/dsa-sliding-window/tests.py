from solution import longest_unique_substring, max_window_sum


def test_max_window_sum_finds_the_best_window():
    got = max_window_sum([2, 1, 5, 1, 3, 2], 3)
    assert got == 9, f"expected 9, got {got!r}"


def test_max_window_sum_with_all_negative_numbers():
    got = max_window_sum([-3, -1, -2], 2)
    assert got == -3, f"expected -3, got {got!r}"


def test_max_window_sum_rejects_impossible_window_sizes():
    for nums, k in [([1, 2], 5), ([1, 2], 0), ([], 1)]:
        got = max_window_sum(nums, k)
        assert got is None, f"max_window_sum({nums!r}, {k}): expected None, got {got!r}"


def test_max_window_sum_when_window_is_the_whole_list():
    got = max_window_sum([4, -1, 2], 3)
    assert got == 5, f"expected 5, got {got!r}"


def test_longest_unique_substring_examples():
    for s, want in [("abcabcbb", 3), ("pwwkew", 3), ("bbbbb", 1), ("abba", 2), ("dvdf", 3)]:
        got = longest_unique_substring(s)
        assert got == want, f"longest_unique_substring({s!r}): expected {want!r}, got {got!r}"


def test_longest_unique_substring_of_empty_string_is_zero():
    got = longest_unique_substring("")
    assert got == 0, f"expected 0, got {got!r}"
