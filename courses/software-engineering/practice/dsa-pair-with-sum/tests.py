from solution import pair_with_sum


class CountingList(list):
    """A list that counts how many items you read and gives up if it's far too many."""

    def __init__(self, items, limit):
        super().__init__(items)
        self.reads, self.limit = 0, limit

    def _count(self, n):
        self.reads += n
        assert self.reads <= self.limit, (
            f"read more than {self.limit} items from a list of {len(self)}: "
            "that's a nested loop, not two pointers"
        )

    def __getitem__(self, index):
        self._count(len(range(len(self))[index]) if isinstance(index, slice) else 1)
        return super().__getitem__(index)

    def __iter__(self):
        for i in range(len(self)):
            self._count(1)
            yield super().__getitem__(i)

    def __contains__(self, value):
        self._count(len(self))
        return super().__contains__(value)


def check_pair(nums, target, got):
    assert got is not None, f"expected a pair summing to {target}, got None"
    i, j = got
    assert 0 <= i < j < len(nums), f"expected indexes with i < j, got {got!r}"
    assert nums[i] + nums[j] == target, f"nums[{i}] + nums[{j}] is {nums[i] + nums[j]}, not {target}"


def test_finds_the_outer_pair():
    got = pair_with_sum([1, 3, 4, 6, 9], 10)
    assert got == (0, 4), f"expected (0, 4), got {got!r}"


def test_finds_a_pair_in_the_middle():
    nums = [1, 3, 4, 6, 9]
    check_pair(nums, 7, pair_with_sum(nums, 7))


def test_returns_none_when_no_pair_exists():
    for nums, target in [([1, 3, 4, 6, 9], 100), ([5], 10), ([], 0)]:
        got = pair_with_sum(nums, target)
        assert got is None, f"pair_with_sum({nums!r}, {target}): expected None, got {got!r}"


def test_uses_two_different_positions_with_duplicates_and_negatives():
    nums = [-4, -1, 2, 2, 7]
    check_pair(nums, 4, pair_with_sum(nums, 4))
    got = pair_with_sum([-4, -1, 3, 7], 6)
    assert got == (1, 3), f"expected (1, 3), got {got!r}"


def test_large_input_in_linear_time():
    n = 100_000
    nums = CountingList(range(0, 2 * n, 2), limit=4 * n)  # 0, 2, 4, ... even numbers
    got = pair_with_sum(nums, 3)  # odd target: no pair exists, so you must scan everything
    assert got is None, f"expected None, got {got!r}"
    target = nums[n // 2] + nums[n // 2 + 1]
    check_pair(list(nums), target, pair_with_sum(CountingList(nums, limit=4 * n), target))
