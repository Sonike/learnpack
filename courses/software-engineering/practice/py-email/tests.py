from solution import is_valid_email


def test_accepts_ordinary_addresses():
    for s in ["ada@example.com", "grace.hopper@navy.mil", "x@y.io"]:
        got = is_valid_email(s)
        assert got is True, f"is_valid_email({s!r}): expected True, got {got!r}"


def test_accepts_plus_tags_and_subdomains():
    for s in ["first.last+news@mail.co.uk", "dev-team@eu.example.org"]:
        got = is_valid_email(s)
        assert got is True, f"is_valid_email({s!r}): expected True, got {got!r}"


def test_rejects_missing_or_doubled_at_sign():
    for s in ["ada.example.com", "ada@@example.com", "a@b@example.com"]:
        got = is_valid_email(s)
        assert got is False, f"is_valid_email({s!r}): expected False, got {got!r}"


def test_rejects_missing_parts():
    for s in ["@example.com", "ada@", "ada@example", "ada@example.c", ""]:
        got = is_valid_email(s)
        assert got is False, f"is_valid_email({s!r}): expected False, got {got!r}"


def test_rejects_spaces_anywhere():
    for s in ["ada @example.com", "ada@exa mple.com", " ada@example.com", "ada@example.com "]:
        got = is_valid_email(s)
        assert got is False, f"is_valid_email({s!r}): expected False, got {got!r}"
