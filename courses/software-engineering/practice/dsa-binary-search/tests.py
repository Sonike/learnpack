import bisect
import random

from solution import binary_search, lower_bound


def test_binary_search_finds_values():
    nums = [1, 3, 5, 7, 9, 11]
    for i, value in enumerate(nums):
        got = binary_search(nums, value)
        assert got == i, f"binary_search({nums!r}, {value}): expected {i}, got {got!r}"


def test_binary_search_returns_minus_one_when_missing():
    for nums, target in [([1, 3, 5, 7, 9, 11], 4), ([1, 3], 0), ([1, 3], 99), ([], 4)]:
        got = binary_search(nums, target)
        assert got == -1, f"binary_search({nums!r}, {target}): expected -1, got {got!r}"


def test_lower_bound_examples():
    nums = [1, 3, 3, 3, 8]
    for target, want in [(3, 1), (4, 4), (9, 5), (0, 0), (8, 4)]:
        got = lower_bound(nums, target)
        assert got == want, f"lower_bound({nums!r}, {target}): expected {want}, got {got!r}"


def test_lower_bound_of_empty_list_is_zero():
    got = lower_bound([], 5)
    assert got == 0, f"expected 0, got {got!r}"


def test_agrees_with_bisect_on_random_lists():
    rng = random.Random(7)
    for _ in range(200):
        nums = sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 30)))
        target = rng.randint(-2, 52)
        want = bisect.bisect_left(nums, target)
        got = lower_bound(nums, target)
        assert got == want, f"lower_bound({nums!r}, {target}): expected {want}, got {got!r}"
        i = binary_search(nums, target)
        if target in nums:
            assert 0 <= i < len(nums) and nums[i] == target, f"binary_search({nums!r}, {target}) gave {i!r}"
        else:
            assert i == -1, f"binary_search({nums!r}, {target}): expected -1, got {i!r}"
