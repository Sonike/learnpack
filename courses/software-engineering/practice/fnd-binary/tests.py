from solution import to_binary, from_binary


def test_small_numbers_convert_to_binary():
    for n, want in [(1, "1"), (2, "10"), (5, "101"), (8, "1000")]:
        got = to_binary(n)
        assert got == want, f"to_binary({n}): expected {want!r}, got {got!r}"


def test_zero_is_a_single_zero():
    got = to_binary(0)
    assert got == "0", f"expected '0', got {got!r}"


def test_to_binary_matches_python_for_0_to_1024():
    for n in range(1025):
        want = bin(n)[2:]
        got = to_binary(n)
        assert got == want, f"to_binary({n}): expected {want!r}, got {got!r}"


def test_from_binary_matches_python_for_0_to_1024():
    for n in range(1025):
        s = bin(n)[2:]
        got = from_binary(s)
        assert got == n, f"from_binary({s!r}): expected {n!r}, got {got!r}"


def test_from_binary_ignores_leading_zeros():
    got = from_binary("00101")
    assert got == 5, f"expected 5, got {got!r}"


def test_round_trip_gives_back_the_number():
    for n in [0, 7, 64, 1000, 65535]:
        got = from_binary(to_binary(n))
        assert got == n, f"from_binary(to_binary({n})): expected {n!r}, got {got!r}"
