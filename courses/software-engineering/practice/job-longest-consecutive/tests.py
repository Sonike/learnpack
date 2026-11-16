from solution import longest_consecutive


def check(nums, want):
    got = longest_consecutive(nums)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_classic_example():
    check([100, 4, 200, 1, 3, 2], 4)


def test_negative_numbers():
    check([0, -1, 1, 2, 9], 4)


def test_duplicates_count_once():
    check([1, 2, 2, 3], 3)


def test_empty_list():
    check([], 0)


def test_single_number():
    check([7], 1)


def test_large_input_runs_in_linear_time():
    nums = list(range(200_000, 0, -1)) + list(range(300_000, 300_010))
    check(nums, 200_000)
