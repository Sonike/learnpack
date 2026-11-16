import re

# TODO: write one compiled regex per rule (see the prompt)


def find_secrets(text: str) -> list[int]:
    """Return 1-based line numbers of lines that look like they contain a secret."""
    flagged = []
    # TODO: loop over text.splitlines() with enumerate(..., start=1)
    # TODO: if any pattern matches the line, append its number
    return flagged


if __name__ == "__main__":
    sample = '''import os
AWS_KEY = "AKIAABCDEFGHIJKLMNOP"
password = os.environ["DB_PASSWORD"]
api_key = "abc123"
SECRET_KEY=
STRIPE_SECRET=whsec_123'''
    print(find_secrets(sample))   # want [2, 4, 6]
