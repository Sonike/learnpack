import random

from solution import range_sum_queries


def test_answers_the_example_queries():
    got = range_sum_queries([3, 1, 4, 1, 5], [(0, 2), (1, 3), (4, 4)])
    assert got == [8, 6, 5], f"expected [8, 6, 5], got {got!r}"


def test_whole_list_query_is_the_total():
    got = range_sum_queries([2, 7, -3], [(0, 2)])
    assert got == [6], f"expected [6], got {got!r}"


def test_handles_negative_numbers():
    got = range_sum_queries([-2, 5, -1, -4], [(1, 2), (2, 3), (0, 0)])
    assert got == [4, -5, -2], f"expected [4, -5, -2], got {got!r}"


def test_no_queries_gives_empty_list():
    got = range_sum_queries([1, 2, 3], [])
    assert got == [], f"expected [], got {got!r}"


def test_matches_slow_answers_on_random_data():
    rng = random.Random(42)
    nums = [rng.randint(-100, 100) for _ in range(500)]
    queries = []
    for _ in range(300):
        a, b = rng.randrange(500), rng.randrange(500)
        queries.append((min(a, b), max(a, b)))
    want = [sum(nums[l : r + 1]) for l, r in queries]
    got = range_sum_queries(nums, queries)
    assert got == want, "some answers differ from summing the slice directly"
