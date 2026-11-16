import math

from solution import celsius_to_fahrenheit, format_temp


def test_freezing_and_boiling_points():
    for c, want in [(0, 32.0), (100, 212.0)]:
        got = celsius_to_fahrenheit(c)
        assert math.isclose(got, want), f"celsius_to_fahrenheit({c}): expected {want!r}, got {got!r}"


def test_minus_forty_is_the_same_on_both_scales():
    got = celsius_to_fahrenheit(-40)
    assert math.isclose(got, -40.0), f"expected -40.0, got {got!r}"


def test_body_temperature():
    got = celsius_to_fahrenheit(37)
    assert math.isclose(got, 98.6), f"expected about 98.6, got {got!r}"


def test_format_uses_one_decimal_place():
    got = format_temp(21.5)
    assert got == "21.5°C = 70.7°F", f"expected '21.5°C = 70.7°F', got {got!r}"


def test_format_whole_and_negative_numbers():
    for c, want in [(0, "0.0°C = 32.0°F"), (-40, "-40.0°C = -40.0°F"), (37, "37.0°C = 98.6°F")]:
        got = format_temp(c)
        assert got == want, f"format_temp({c}): expected {want!r}, got {got!r}"
