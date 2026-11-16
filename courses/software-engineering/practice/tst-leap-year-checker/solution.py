def check_is_leap_year(fn) -> None:
    """Assert that fn(year) follows the leap-year rule. Raise AssertionError if it doesn't."""
    assert fn(2024) is True, "2024 is divisible by 4, so it is a leap year"
    assert fn(2023) is False, "2023 is not divisible by 4, so it is not a leap year"
    assert fn(1900) is False, "1900 is divisible by 100 but not 400, so it is not a leap year"
    assert fn(2000) is True, "2000 is divisible by 400, so it is a leap year"


if __name__ == "__main__":
    check_is_leap_year(lambda y: y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
    print("correct version passed")
