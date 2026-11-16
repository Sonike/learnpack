from solution import URLShortener, decode, encode


def test_encodes_known_values():
    got = [encode(0), encode(9), encode(10), encode(61), encode(62), encode(125), encode(62**3)]
    want = ["0", "9", "a", "Z", "10", "21", "1000"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_decode_reverses_encode():
    bad = [n for n in list(range(5000)) + [10**12, 2**63] if decode(encode(n)) != n]
    assert bad == [], f"expected no failures, got {bad[:5]!r}"


def test_rejects_negative_numbers_and_invalid_codes():
    got = []
    for call in (lambda: encode(-1), lambda: decode("ab-c"), lambda: decode("")):
        try:
            call()
            got.append(None)
        except ValueError as e:
            got.append(str(e))
    want = ["n must be 0 or more", "invalid code: 'ab-c'", "invalid code: ''"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_shorten_and_expand_round_trip():
    s = URLShortener()
    a = s.shorten("https://example.com/a")
    b = s.shorten("https://example.com/b")
    again = s.shorten("https://example.com/a")
    got = (a, b, again, s.expand(b), s.expand("zz"), s.expand("!!"))
    want = ("1", "2", "1", "https://example.com/b", None, None)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ten_thousand_urls_get_unique_codes():
    s = URLShortener()
    urls = [f"https://example.com/page/{i}" for i in range(10_000)]
    codes = [s.shorten(u) for u in urls]
    got = (len(set(codes)), all(s.expand(c) == u for c, u in zip(codes, urls)), max(len(c) for c in codes))
    want = (10_000, True, 3)
    assert got == want, f"expected {want!r}, got {got!r}"
