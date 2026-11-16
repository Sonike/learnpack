from solution import parse_age


def raised_message(text):
    """Call parse_age and return the ValueError message, or None if nothing was raised."""
    try:
        parse_age(text)
    except ValueError as e:
        return str(e)
    return None


def test_parses_a_plain_number():
    got = parse_age("42")
    assert got == 42, f"expected 42, got {got!r}"


def test_strips_surrounding_whitespace():
    got = parse_age("  7\n")
    assert got == 7, f"expected 7, got {got!r}"


def test_accepts_the_edges_of_the_range():
    assert parse_age("0") == 0, "0 is a valid age"
    assert parse_age("150") == 150, "150 is a valid age"


def test_rejects_text_that_is_not_a_number():
    for text in ["abc", "4.5", ""]:
        msg = raised_message(text)
        assert msg is not None, f"expected ValueError for {text!r}, nothing was raised"
        assert repr(text) in msg, f"the message should quote the input {text!r}, got {msg!r}"


def test_rejects_negative_and_too_large_ages():
    for text in ["-1", "151", "999"]:
        msg = raised_message(text)
        assert msg is not None, f"expected ValueError for {text!r}, nothing was raised"
        assert "between 0 and 150" in msg, f"expected the range in the message, got {msg!r}"
