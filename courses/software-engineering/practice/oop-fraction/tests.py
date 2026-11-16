from solution import Fraction


def test_reduces_on_creation():
    f = Fraction(6, 8)
    got = (f.numerator, f.denominator)
    assert got == (3, 4), f"expected (3, 4), got {got!r}"


def test_adds_two_fractions():
    got = Fraction(1, 2) + Fraction(1, 3)
    assert (got.numerator, got.denominator) == (5, 6), f"expected 5/6, got {got!r}"
    got = Fraction(1, 4) + Fraction(1, 4)
    assert (got.numerator, got.denominator) == (1, 2), f"expected 1/4 + 1/4 to reduce to 1/2, got {got!r}"


def test_equal_values_compare_equal():
    assert Fraction(1, 2) == Fraction(2, 4), "expected Fraction(1, 2) == Fraction(2, 4)"
    assert Fraction(1, 2) != Fraction(1, 3), "expected Fraction(1, 2) != Fraction(1, 3)"
    assert Fraction(1, 2) != "1/2", "a Fraction should not equal a string"


def test_repr_looks_like_the_constructor_call():
    got = repr(Fraction(10, 20))
    assert got == "Fraction(1, 2)", f"expected 'Fraction(1, 2)', got {got!r}"


def test_negative_denominator_moves_sign_to_numerator():
    f = Fraction(1, -2)
    got = (f.numerator, f.denominator)
    assert got == (-1, 2), f"expected (-1, 2), got {got!r}"
    z = Fraction(0, -5)
    assert (z.numerator, z.denominator) == (0, 1), f"expected zero to be stored as 0/1, got {z!r}"


def test_zero_denominator_raises():
    try:
        Fraction(1, 0)
    except ZeroDivisionError:
        return
    raise AssertionError("Fraction(1, 0) should raise ZeroDivisionError")
