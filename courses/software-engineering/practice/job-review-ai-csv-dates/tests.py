from datetime import datetime, timezone

from solution import parse_csv_dates

UTC = timezone.utc


def test_converts_offsets_to_utc():
    text = "id,at\n1,2026-03-01T09:30:00+01:00\n2,2026-03-01T20:00:00-05:00\n"
    got = parse_csv_dates(text, "at")
    want = [datetime(2026, 3, 1, 8, 30, tzinfo=UTC), datetime(2026, 3, 2, 1, 0, tzinfo=UTC)]
    assert got == want, f"expected {want!r}, got {got!r}"
    assert all(d.utcoffset().total_seconds() == 0 for d in got), "every result must have a UTC offset of 0"


def test_value_without_offset_is_treated_as_utc():
    got = parse_csv_dates("id,at\n1,2026-03-01T12:00:00\n", "at")
    want = [datetime(2026, 3, 1, 12, 0, tzinfo=UTC)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_first_data_row_is_not_skipped():
    text = "id,at\n1,2026-01-01T00:00:00+00:00\n2,2026-01-02T00:00:00+00:00\n"
    got = len(parse_csv_dates(text, "at"))
    assert got == 2, f"expected 2 dates, got {got!r}"


def test_empty_values_are_skipped():
    text = "id,at\n1,\n2,2026-01-02T00:00:00\n3,  \n"
    got = parse_csv_dates(text, "at")
    want = [datetime(2026, 1, 2, tzinfo=UTC)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_bad_date_raises_with_line_number():
    text = "id,at\n1,2026-01-01T00:00:00\n2,yesterday\n"
    try:
        parse_csv_dates(text, "at")
    except ValueError as err:
        assert "line 3" in str(err), f"expected 'line 3' in the message, got {str(err)!r}"
    else:
        assert False, "expected a ValueError for 'yesterday', but nothing was raised"
