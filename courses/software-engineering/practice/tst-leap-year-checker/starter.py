def check_is_leap_year(fn) -> None:
    """Assert that fn(year) follows the leap-year rule. Raise AssertionError if it doesn't."""
    # TODO: an ordinary leap year, an ordinary non-leap year,
    #       a century that isn't a leap year, and a century that is.
    pass


if __name__ == "__main__":
    def correct(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def only_checks_4(year):
        return year % 4 == 0

    for candidate in (correct, only_checks_4):
        try:
            check_is_leap_year(candidate)
            print(candidate.__name__, "passed")
        except AssertionError as e:
            print(candidate.__name__, "caught:", e)
