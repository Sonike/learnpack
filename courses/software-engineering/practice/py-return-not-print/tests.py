from solution import average, format_price


def test_average_returns_the_mean():
    got = average([1, 2, 3, 4])
    assert got == 2.5, f"expected 2.5, got {got!r} (did you return instead of print?)"


def test_average_of_one_number():
    got = average([7])
    assert got == 7, f"expected 7, got {got!r}"


def test_average_of_empty_list_is_none():
    got = average([])
    assert got is None, f"expected None, got {got!r}"


def test_format_price_returns_text_with_two_decimals():
    for amount, want in [(3.5, "$3.50"), (10, "$10.00"), (1234.5, "$1234.50")]:
        got = format_price(amount)
        assert got == want, f"format_price({amount}): expected {want!r}, got {got!r}"


def test_functions_compose():
    got = format_price(average([2, 4]))
    assert got == "$3.00", f"expected '$3.00', got {got!r}"
