from solution import is_leap_year


def test_ordinary_year_is_not_leap():
    for year in [2023, 2019, 1]:
        got = is_leap_year(year)
        assert got is False, f"is_leap_year({year}): expected False, got {got!r}"


def test_divisible_by_four_is_leap():
    for year in [2024, 1996, 4]:
        got = is_leap_year(year)
        assert got is True, f"is_leap_year({year}): expected True, got {got!r}"


def test_century_years_are_not_leap():
    for year in [1900, 2100, 1800]:
        got = is_leap_year(year)
        assert got is False, f"is_leap_year({year}): expected False, got {got!r}"


def test_years_divisible_by_400_are_leap():
    for year in [2000, 1600, 2400]:
        got = is_leap_year(year)
        assert got is True, f"is_leap_year({year}): expected True, got {got!r}"
