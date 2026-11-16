import dataclasses

from solution import Money


def test_adds_same_currency():
    got = Money(1250, "USD") + Money(100, "USD")
    assert got == Money(1350, "USD"), f"expected Money(1350, 'USD'), got {got!r}"


def test_refuses_mixed_currencies():
    try:
        Money(1250, "USD") + Money(500, "EUR")
    except ValueError:
        return
    raise AssertionError("adding USD to EUR should raise ValueError")


def test_is_frozen():
    price = Money(1250, "USD")
    try:
        price.amount_cents = 0
    except dataclasses.FrozenInstanceError:
        pass
    else:
        raise AssertionError("assigning to a field should raise FrozenInstanceError (use frozen=True)")
    assert price.amount_cents == 1250, f"expected 1250, got {price.amount_cents!r}"


def test_equal_values_work_in_a_set():
    got = {Money(100, "USD"), Money(100, "USD"), Money(100, "EUR")}
    assert len(got) == 2, f"expected 2 distinct values, got {got!r}"


def test_str_formats_two_decimals():
    for money, want in [(Money(1250, "USD"), "12.50 USD"), (Money(5, "USD"), "0.05 USD"), (Money(0, "GBP"), "0.00 GBP")]:
        got = str(money)
        assert got == want, f"expected {want!r}, got {got!r}"


def test_str_handles_negative_amounts():
    got = str(Money(-250, "EUR"))
    assert got == "-2.50 EUR", f"expected '-2.50 EUR', got {got!r}"
