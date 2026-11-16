from solution import split_bill


def test_even_split_without_tip():
    got = split_bill(100, 4, 0)
    assert got == 25.0, f"expected 25.0, got {got!r}"


def test_rounds_to_cents():
    got = split_bill(100, 3, 0)
    assert got == 33.33, f"expected 33.33, got {got!r}"


def test_adds_the_tip_before_splitting():
    got = split_bill(120, 4, 15)
    assert got == 34.5, f"expected 34.5, got {got!r}"


def test_rounds_once_at_the_end():
    got = split_bill(59.99, 2, 10)
    assert got == 32.99, f"expected 32.99 (65.989 / 2 = 32.9945), got {got!r}"


def test_one_person_pays_everything():
    got = split_bill(48.5, 1, 20)
    assert got == 58.2, f"expected 58.2, got {got!r}"
