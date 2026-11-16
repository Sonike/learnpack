MIN_AGE = 0
MAX_AGE = 150


def parse_age(s: str) -> int:
    """Turn user-typed text into an age from 0 to 150, or raise ValueError."""
    try:
        age = int(s.strip())
    except ValueError:
        raise ValueError(f"age must be a whole number, got {s!r}") from None

    if not MIN_AGE <= age <= MAX_AGE:
        raise ValueError(f"age must be between {MIN_AGE} and {MAX_AGE}, got {age}")
    return age
