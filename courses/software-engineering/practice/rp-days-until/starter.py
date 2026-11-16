from datetime import date


def days_until(date_str: str, today: date) -> int:
    """Days from today to date_str ("YYYY-MM-DD"). Negative if it's in the past."""
    # TODO: turn date_str into a date with date.fromisoformat
    # TODO: subtracting two dates gives a timedelta; return its .days
    return 0


if __name__ == "__main__":
    today = date(2026, 11, 13)
    print(days_until("2026-12-25", today))  # want 42
    print(days_until("2026-11-10", today))  # want -3
