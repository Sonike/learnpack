from solution import RecentCounter


def test_counts_pings_in_the_window():
    c = RecentCounter(3000)
    got = [c.ping(t) for t in [1, 100, 3001, 3002]]
    assert got == [1, 2, 3, 3], f"expected [1, 2, 3, 3], got {got!r}"


def test_window_edge_is_included():
    c = RecentCounter(10)
    c.ping(0)
    got = c.ping(10)
    assert got == 2, f"a ping exactly 10 seconds ago still counts: expected 2, got {got!r}"


def test_old_pings_all_drop_out_after_a_long_gap():
    c = RecentCounter(5)
    for t in [1, 2, 3, 4]:
        c.ping(t)
    got = c.ping(100)
    assert got == 1, f"expected 1, got {got!r}"


def test_pings_at_the_same_time_all_count():
    c = RecentCounter(1)
    got = [c.ping(7), c.ping(7), c.ping(7)]
    assert got == [1, 2, 3], f"expected [1, 2, 3], got {got!r}"


def test_memory_stays_small():
    c = RecentCounter(10)
    for t in range(100_000):
        c.ping(t)
    assert len(c.times) == 11, f"only the last 11 pings should be kept, got {len(c.times)}"
