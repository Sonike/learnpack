def bmi(weight_kg: float, height_m: float) -> float:
    """Return body-mass index: weight divided by height squared."""
    # TODO
    return 0.0


def bmi_category(value: float) -> str:
    """Return "underweight", "normal", "overweight" or "obese" for a BMI value."""
    # TODO: use if/elif/else with the boundaries 18.5, 25 and 30
    return ""


def bmi_report(weight_kg: float, height_m: float) -> str:
    """Return text like "BMI 22.9 (normal)"."""
    # TODO: call bmi(), then bmi_category(), then build the text with an f-string
    return ""


if __name__ == "__main__":
    print(bmi(70, 1.75))
    print(bmi_report(70, 1.75))   # BMI 22.9 (normal)
