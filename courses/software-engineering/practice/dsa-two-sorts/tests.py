import random

from solution import insertion_sort, merge_sort

SORTS = (insertion_sort, merge_sort)


def test_sorts_a_small_list():
    for fn in SORTS:
        got = fn([5, 2, 9, 1, 5])
        assert got == [1, 2, 5, 5, 9], f"{fn.__name__}: expected [1, 2, 5, 5, 9], got {got!r}"


def test_empty_and_single_item_lists():
    for fn in SORTS:
        for items in ([], [42]):
            got = fn(items)
            assert got == items, f"{fn.__name__}({items!r}): expected {items!r}, got {got!r}"


def test_does_not_change_the_input():
    for fn in SORTS:
        items = [3, 1, 2]
        fn(items)
        assert items == [3, 1, 2], f"{fn.__name__} changed its input to {items!r}"


def test_matches_sorted_on_random_lists():
    rng = random.Random(2024)
    for _ in range(50):
        items = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
        for fn in SORTS:
            got = fn(items)
            assert got == sorted(items), f"{fn.__name__}({items!r}) gave {got!r}"


def test_sorts_by_key():
    words = ["pear", "fig", "apple", "kiwi"]
    for fn in SORTS:
        got = fn(words, key=len)
        assert got == ["fig", "pear", "kiwi", "apple"], f"{fn.__name__}: got {got!r}"


def test_is_stable():
    rng = random.Random(5)
    records = [(rng.randint(1, 5), i) for i in range(80)]  # (grade, original position)
    want = sorted(records, key=lambda r: r[0])
    for fn in SORTS:
        got = fn(records, key=lambda r: r[0])
        assert got == want, f"{fn.__name__} reordered records with equal keys"
