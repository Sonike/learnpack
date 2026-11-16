from datetime import date

from solution import days_until

TODAY = date(2026, 11, 13)


def test_counts_days_to_a_future_date():
    got = days_until("2026-12-25", TODAY)
    assert got == 42, f"expected 42, got {got!r}"


def test_today_is_zero():
    got = days_until("2026-11-13", TODAY)
    assert got == 0, f"expected 0, got {got!r}"


def test_past_dates_are_negative():
    got = days_until("2026-11-10", TODAY)
    assert got == -3, f"expected -3, got {got!r}"


def test_leap_years_are_handled():
    got = days_until("2028-03-01", date(2028, 2, 28))
    assert got == 2, f"2028 is a leap year (Feb 29 exists): expected 2, got {got!r}"


def test_invalid_dates_raise_value_error():
    for bad in ["2026-02-30", "next friday", ""]:
        try:
            days_until(bad, TODAY)
        except ValueError:
            continue
        assert False, f"expected ValueError for {bad!r}"
