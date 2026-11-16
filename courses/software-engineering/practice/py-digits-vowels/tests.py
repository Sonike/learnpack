from solution import sum_of_digits, count_vowels


def test_sum_of_digits_of_a_normal_number():
    got = sum_of_digits(1234)
    assert got == 10, f"expected 10, got {got!r}"


def test_sum_of_digits_of_zero_and_single_digit():
    for n, want in [(0, 0), (7, 7), (1000, 1)]:
        got = sum_of_digits(n)
        assert got == want, f"sum_of_digits({n}): expected {want!r}, got {got!r}"


def test_sum_of_digits_of_negative_number():
    got = sum_of_digits(-505)
    assert got == 10, f"expected 10, got {got!r}"


def test_count_vowels_ignores_case():
    got = count_vowels("Hello World AEIOU")
    assert got == 8, f"expected 8, got {got!r}"


def test_count_vowels_with_none_or_empty():
    for s in ["rhythm", "", "123 !?"]:
        got = count_vowels(s)
        assert got == 0, f"count_vowels({s!r}): expected 0, got {got!r}"
