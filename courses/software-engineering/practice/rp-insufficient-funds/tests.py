from solution import InsufficientFunds, withdraw


def test_withdraw_returns_the_new_balance():
    got = withdraw(100.0, 30.0)
    assert got == 70.0, f"expected 70.0, got {got!r}"


def test_withdrawing_the_whole_balance_is_allowed():
    got = withdraw(25.0, 25.0)
    assert got == 0.0, f"expected 0.0, got {got!r}"


def test_insufficient_funds_is_an_exception():
    assert issubclass(InsufficientFunds, Exception), "InsufficientFunds should subclass Exception"


def test_overdraw_raises_insufficient_funds_with_the_shortfall():
    try:
        withdraw(30.0, 50.0)
    except InsufficientFunds as e:
        assert e.shortfall == 20.0, f"expected shortfall 20.0, got {e.shortfall!r}"
        want = "cannot withdraw 50.00: balance is 30.00, short by 20.00"
        assert str(e) == want, f"expected {want!r}, got {str(e)!r}"
        return
    assert False, "expected InsufficientFunds to be raised"


def test_rejects_zero_and_negative_amounts():
    for amount in [0, -5.0]:
        try:
            withdraw(100.0, amount)
        except ValueError as e:
            assert "positive" in str(e), f"expected 'positive' in the message, got {str(e)!r}"
            continue
        assert False, f"expected ValueError for amount {amount!r}"
