def celsius_to_fahrenheit(c: float) -> float:
    """Convert degrees Celsius to degrees Fahrenheit."""
    return c * 9 / 5 + 32


def format_temp(c: float) -> str:
    """Return text like "21.5°C = 70.7°F", one decimal place each."""
    f = celsius_to_fahrenheit(c)
    return f"{c:.1f}°C = {f:.1f}°F"


if __name__ == "__main__":
    print(celsius_to_fahrenheit(100))   # should be 212.0
    print(format_temp(21.5))            # should be 21.5°C = 70.7°F
