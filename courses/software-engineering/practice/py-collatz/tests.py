from solution import collatz_steps


def test_one_takes_zero_steps():
    got = collatz_steps(1)
    assert got == 0, f"expected 0, got {got!r}"


def test_powers_of_two_just_halve():
    for n, want in [(2, 1), (8, 3), (1024, 10)]:
        got = collatz_steps(n)
        assert got == want, f"collatz_steps({n}): expected {want!r}, got {got!r}"


def test_six_takes_eight_steps():
    got = collatz_steps(6)
    assert got == 8, f"expected 8, got {got!r}"


def test_twenty_seven_takes_a_long_trip():
    got = collatz_steps(27)
    assert got == 111, f"expected 111, got {got!r}"


def test_returns_an_int():
    got = collatz_steps(7)
    assert got == 16 and type(got) is int, f"expected the int 16, got {got!r}"
