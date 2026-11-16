from solution import LRUCache, TTLCache


def test_get_returns_stored_values_and_default_for_missing():
    cache = LRUCache(2)
    cache.put("a", 1)
    got = (cache.get("a"), cache.get("zzz"), cache.get("zzz", -1))
    want = (1, None, -1)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_evicts_the_least_recently_used_entry():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    got = (cache.get("a"), cache.get("b"), cache.get("c"), len(cache))
    want = (1, None, 3, 2)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_updating_a_key_replaces_it_and_marks_it_recent():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    got = (cache.get("a"), cache.get("b"), len(cache))
    want = (10, None, 2)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_rejects_capacity_below_one():
    try:
        LRUCache(0)
    except ValueError as e:
        got = str(e)
    else:
        got = None
    want = "capacity must be at least 1"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ttl_entries_expire_exactly_at_ttl():
    clock = [100.0]
    cache = TTLCache(10, ttl=60, now=lambda: clock[0])
    cache.put("rate", 0.92)
    clock[0] = 159.9
    before = cache.get("rate")
    clock[0] = 160.0
    after = cache.get("rate", "gone")
    got = (before, after, len(cache))
    want = (0.92, "gone", 0)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ttl_put_resets_expiry_and_lru_still_applies():
    clock = [0.0]
    cache = TTLCache(2, ttl=10, now=lambda: clock[0])
    cache.put("a", 1)
    clock[0] = 8.0
    cache.put("a", 2)
    clock[0] = 15.0
    refreshed = cache.get("a")
    cache.put("b", 3)
    cache.put("c", 4)
    got = (refreshed, cache.get("a"), cache.get("c"))
    want = (2, None, 4)
    assert got == want, f"expected {want!r}, got {got!r}"
