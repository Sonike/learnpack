from solution import check_regression, split_bill


def buggy(total_cents, people):
    share = total_cents // people
    return [share] * people


def rounds_everyone_up(total_cents, people):
    share = -(-total_cents // people)
    return [share] * people


def correct(total_cents, people):
    share, leftover = divmod(total_cents, people)
    return [share + 1 if i < leftover else share for i in range(people)]


def caught(fn):
    try:
        check_regression(fn)
    except Exception:
        return True
    return False


def test_regression_test_fails_on_the_buggy_version():
    assert caught(buggy), "your check_regression passed the buggy version, so it doesn't reproduce the bug"


def test_regression_test_passes_on_a_correct_version():
    try:
        check_regression(correct)
    except AssertionError as e:
        raise AssertionError(f"your check_regression rejected a correct split_bill: {e}") from None


def test_regression_test_catches_overcharging():
    assert caught(rounds_everyone_up), "your check_regression passed a version that charges 10.02 for a 10.00 bill"


def test_split_bill_gives_leftover_cents_to_the_first_people():
    for args, want in [((1000, 3), [334, 333, 333]), ((1001, 3), [334, 334, 333]), ((900, 3), [300, 300, 300]), ((5, 1), [5])]:
        got = split_bill(*args)
        assert got == want, f"split_bill{args}: expected {want!r}, got {got!r}"


def test_split_bill_rejects_zero_people():
    try:
        split_bill(1000, 0)
    except ValueError:
        return
    raise AssertionError("split_bill(1000, 0) should raise ValueError")
