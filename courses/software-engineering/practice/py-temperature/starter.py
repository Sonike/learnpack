def celsius_to_fahrenheit(c: float) -> float:
    """Convert degrees Celsius to degrees Fahrenheit."""
    # TODO: F = C * 9 / 5 + 32
    return 0.0


def format_temp(c: float) -> str:
    """Return text like "21.5°C = 70.7°F", one decimal place each."""
    # TODO: call celsius_to_fahrenheit, then build the text with an f-string and :.1f
    return ""


if __name__ == "__main__":
    print(celsius_to_fahrenheit(100))   # should be 212.0
    print(format_temp(21.5))            # should be 21.5°C = 70.7°F
