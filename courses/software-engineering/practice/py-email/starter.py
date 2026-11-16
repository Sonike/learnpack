import re

# TODO: write the pattern described in the task as a raw string
EMAIL_PATTERN = r""


def is_valid_email(s: str) -> bool:
    """Return True if s looks like an email address (a deliberately simple check)."""
    # TODO: use re.fullmatch(EMAIL_PATTERN, s) and turn the result into True/False
    return False


if __name__ == "__main__":
    for s in ["ada@example.com", "ada.example.com", "ada@example", "ada @example.com"]:
        print(repr(s), is_valid_email(s))
