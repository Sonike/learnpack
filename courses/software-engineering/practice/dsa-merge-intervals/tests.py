from solution import merge_intervals


def check(intervals, want):
    got = merge_intervals(intervals)
    assert got == want, f"merge_intervals({intervals!r}): expected {want!r}, got {got!r}"


def test_merges_unsorted_overlapping_intervals():
    check([(8, 10), (1, 3), (2, 6), (15, 18)], [(1, 6), (8, 10), (15, 18)])


def test_touching_intervals_merge():
    check([(1, 4), (4, 5)], [(1, 5)])


def test_interval_inside_another_disappears():
    check([(1, 10), (2, 3), (4, 5)], [(1, 10)])


def test_empty_and_single_inputs():
    check([], [])
    check([(3, 3)], [(3, 3)])


def test_does_not_change_the_input():
    intervals = [(5, 6), (1, 2)]
    merge_intervals(intervals)
    assert intervals == [(5, 6), (1, 2)], f"the input was changed to {intervals!r}"
