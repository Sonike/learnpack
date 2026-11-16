import math

from solution import classify_growth

SIZES = [1000, 2000, 4000, 8000]


def check(steps, want):
    got = classify_growth(SIZES, steps)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_spots_linear_growth_despite_constants():
    check([3 * n + 5 for n in SIZES], "O(n)")


def test_spots_quadratic_growth():
    check([n * n // 2 for n in SIZES], "O(n^2)")


def test_spots_constant_time():
    check([7, 7, 7, 7], "O(1)")


def test_spots_logarithmic_growth():
    check([round(math.log2(n)) + 1 for n in SIZES], "O(log n)")


def test_tells_n_log_n_apart_from_n():
    check([round(2 * n * math.log2(n)) for n in SIZES], "O(n log n)")


def test_works_with_just_two_sizes():
    got = classify_growth([50, 100], [2500, 10000])
    assert got == "O(n^2)", f"expected 'O(n^2)', got {got!r}"
