def is_leap_year(year: int) -> bool:
    """Return True if year is a leap year in the Gregorian calendar."""
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    for y in [2023, 2024, 1900, 2000, 2100]:
        print(y, is_leap_year(y))
