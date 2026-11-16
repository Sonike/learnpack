from solution import min_meeting_rooms


def check(intervals, want):
    got = min_meeting_rooms(intervals)
    assert got == want, f"expected {want!r} for {intervals!r}, got {got!r}"


def test_classic_example_needs_two_rooms():
    check([(0, 30), (5, 10), (15, 20)], 2)


def test_unsorted_non_overlapping_needs_one_room():
    check([(7, 10), (2, 4)], 1)


def test_back_to_back_meetings_share_a_room():
    check([(1, 5), (5, 9), (9, 12)], 1)


def test_no_meetings_needs_no_rooms():
    check([], 0)


def test_all_at_once_needs_one_room_each():
    check([(0, 10)] * 4, 4)


def test_large_input_is_fast():
    meetings = [(i, i + 3) for i in range(50_000)]
    check(meetings, 3)
