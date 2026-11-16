from datetime import date


def days_until(date_str: str, today: date) -> int:
    """Days from today to date_str ("YYYY-MM-DD"). Negative if it's in the past."""
    target = date.fromisoformat(date_str)
    return (target - today).days
