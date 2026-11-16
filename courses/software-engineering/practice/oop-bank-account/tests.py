from solution import BankAccount


def test_deposit_and_withdraw_change_the_balance():
    account = BankAccount("Ada")
    account.deposit(2000)
    account.withdraw(750)
    assert account.balance == 1250, f"expected 1250, got {account.balance!r}"


def test_overdraft_is_refused_and_balance_unchanged():
    account = BankAccount("Ada")
    account.deposit(100)
    try:
        account.withdraw(500)
    except ValueError:
        pass
    else:
        raise AssertionError("withdrawing more than the balance should raise ValueError")
    assert account.balance == 100, f"expected the balance to stay 100, got {account.balance!r}"


def test_rejects_zero_and_negative_amounts():
    account = BankAccount("Ada")
    for action, amount in [("deposit", 0), ("deposit", -5), ("withdraw", 0), ("withdraw", -5)]:
        try:
            getattr(account, action)(amount)
        except ValueError:
            continue
        raise AssertionError(f"{action}({amount}) should raise ValueError")


def test_balance_is_read_only():
    account = BankAccount("Ada")
    try:
        account.balance = 1_000_000
    except AttributeError:
        pass
    else:
        raise AssertionError("assigning to account.balance should raise AttributeError (use a property without a setter)")
    assert account.balance == 0, f"expected 0, got {account.balance!r}"


def test_history_records_successes_only_and_is_a_copy():
    account = BankAccount("Ada")
    account.deposit(2000)
    account.withdraw(750)
    try:
        account.withdraw(99_999)
    except ValueError:
        pass
    want = [("deposit", 2000), ("withdraw", 750)]
    assert account.history == want, f"expected {want!r}, got {account.history!r}"
    account.history.append(("deposit", 1))
    assert account.history == want, "changing the returned list must not change the account's real history"


def test_repr_shows_owner_and_balance():
    account = BankAccount("Ada")
    account.deposit(1250)
    want = "BankAccount(owner='Ada', balance=1250)"
    assert repr(account) == want, f"expected {want!r}, got {repr(account)!r}"
