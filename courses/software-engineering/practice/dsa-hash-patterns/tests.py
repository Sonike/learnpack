from solution import first_unique_char, group_anagrams, two_sum


def test_two_sum_finds_the_pair():
    for nums, target, want in [([2, 7, 11, 15], 9, (0, 1)), ([3, 2, 4], 6, (1, 2)), ([3, 3], 6, (0, 1))]:
        got = two_sum(nums, target)
        assert got == want, f"two_sum({nums!r}, {target}): expected {want!r}, got {got!r}"


def test_two_sum_does_not_use_one_number_twice():
    got = two_sum([3, 5], 6)
    assert got is None, f"3 + 3 would reuse index 0: expected None, got {got!r}"


def test_two_sum_on_empty_list():
    got = two_sum([], 1)
    assert got is None, f"expected None, got {got!r}"


def test_group_anagrams_keeps_first_seen_order():
    got = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    want = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_group_anagrams_of_nothing_is_empty():
    got = group_anagrams([])
    assert got == [], f"expected [], got {got!r}"


def test_first_unique_char():
    for s, want in [("leetcode", 0), ("loveleetcode", 2), ("aabb", -1), ("", -1), ("z", 0)]:
        got = first_unique_char(s)
        assert got == want, f"first_unique_char({s!r}): expected {want!r}, got {got!r}"
