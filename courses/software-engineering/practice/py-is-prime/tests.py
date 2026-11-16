from solution import is_prime


def test_numbers_below_two_are_not_prime():
    for n in [-7, 0, 1]:
        got = is_prime(n)
        assert got is False, f"is_prime({n}): expected False, got {got!r}"


def test_two_and_three_are_prime():
    for n in [2, 3]:
        got = is_prime(n)
        assert got is True, f"is_prime({n}): expected True, got {got!r}"


def test_primes_below_fifty():
    want = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    got = [n for n in range(50) if is_prime(n)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_squares_of_primes_are_not_prime():
    for n in [4, 9, 25, 49, 121]:
        got = is_prime(n)
        assert got is False, f"is_prime({n}): expected False (check your <= in the loop), got {got!r}"


def test_large_prime_is_fast():
    got = is_prime(1_000_000_007)
    assert got is True, f"expected True, got {got!r}"
    got = is_prime(999_999_999)
    assert got is False, f"999,999,999 is divisible by 3: expected False, got {got!r}"
