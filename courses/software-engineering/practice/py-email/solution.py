import re

EMAIL_PATTERN = r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}"


def is_valid_email(s: str) -> bool:
    """Return True if s looks like an email address (a deliberately simple check)."""
    return re.fullmatch(EMAIL_PATTERN, s) is not None


if __name__ == "__main__":
    for s in ["ada@example.com", "ada.example.com", "ada@example", "ada @example.com"]:
        print(repr(s), is_valid_email(s))
