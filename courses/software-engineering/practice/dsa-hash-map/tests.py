from solution import HashMap


class SameHash:
    """A key whose hash is always 42, so every SameHash key collides."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, SameHash) and self.name == other.name


def test_put_and_get():
    m = HashMap()
    m.put("apple", 3)
    m.put("pear", 5)
    got = (m.get("apple"), m.get("pear"), m.get("kiwi"), m.get("kiwi", 0))
    assert got == (3, 5, None, 0), f"expected (3, 5, None, 0), got {got!r}"


def test_put_existing_key_replaces_value():
    m = HashMap()
    m.put("apple", 3)
    m.put("apple", 4)
    got = (m.get("apple"), len(m))
    assert got == (4, 1), f"expected (value 4, length 1), got {got!r}"


def test_remove_returns_whether_key_was_there():
    m = HashMap()
    m.put("pear", 5)
    got = (m.remove("pear"), m.remove("pear"), len(m), m.get("pear"))
    assert got == (True, False, 0, None), f"expected (True, False, 0, None), got {got!r}"


def test_colliding_keys_are_kept_apart():
    m = HashMap()
    a, b, c = SameHash("a"), SameHash("b"), SameHash("c")
    m.put(a, 1)
    m.put(b, 2)
    m.put(c, 3)
    m.remove(b)
    got = (m.get(SameHash("a")), m.get(SameHash("b")), m.get(SameHash("c")), len(m))
    assert got == (1, None, 3, 2), f"expected (1, None, 3, 2), got {got!r}"


def test_resizes_when_load_factor_passes_three_quarters():
    m = HashMap()
    for i in range(6):
        m.put(i, i)
    assert len(m.buckets) == 8, f"6/8 = 0.75 is not over the limit: expected 8 buckets, got {len(m.buckets)}"
    m.put(6, 6)
    assert len(m.buckets) == 16, f"7/8 > 0.75: expected 16 buckets, got {len(m.buckets)}"


def test_every_key_survives_many_resizes():
    m = HashMap()
    for i in range(1000):
        m.put(f"user{i}", i * i)
    wrong = [i for i in range(1000) if m.get(f"user{i}") != i * i]
    assert not wrong, f"lost or wrong values for keys like user{wrong[:3]}"
    assert len(m) == 1000, f"expected 1000, got {len(m)}"
