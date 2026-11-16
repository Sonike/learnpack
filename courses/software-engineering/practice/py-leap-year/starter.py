def is_leap_year(year: int) -> bool:
    """Return True if year is a leap year in the Gregorian calendar."""
    # TODO: check the most specific rule (400) first, then 100, then 4
    return False


if __name__ == "__main__":
    for y in [2023, 2024, 1900, 2000, 2100]:
        print(y, is_leap_year(y))
