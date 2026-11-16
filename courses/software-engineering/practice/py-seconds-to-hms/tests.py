from solution import seconds_to_hms


def test_hours_minutes_and_seconds():
    got = seconds_to_hms(3723)
    assert got == "01:02:03", f"expected '01:02:03', got {got!r}"


def test_zero_seconds():
    got = seconds_to_hms(0)
    assert got == "00:00:00", f"expected '00:00:00', got {got!r}"


def test_exact_boundaries():
    for s, want in [(59, "00:00:59"), (60, "00:01:00"), (3599, "00:59:59"), (3600, "01:00:00")]:
        got = seconds_to_hms(s)
        assert got == want, f"seconds_to_hms({s}): expected {want!r}, got {got!r}"


def test_last_second_of_the_day():
    got = seconds_to_hms(86399)
    assert got == "23:59:59", f"expected '23:59:59', got {got!r}"


def test_hours_do_not_wrap_at_24():
    got = seconds_to_hms(360000)
    assert got == "100:00:00", f"expected '100:00:00', got {got!r}"
