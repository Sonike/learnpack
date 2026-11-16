def bmi(weight_kg: float, height_m: float) -> float:
    """Return body-mass index: weight divided by height squared."""
    return weight_kg / height_m ** 2


def bmi_category(value: float) -> str:
    """Return "underweight", "normal", "overweight" or "obese" for a BMI value."""
    if value < 18.5:
        return "underweight"
    elif value < 25:
        return "normal"
    elif value < 30:
        return "overweight"
    else:
        return "obese"


def bmi_report(weight_kg: float, height_m: float) -> str:
    """Return text like "BMI 22.9 (normal)"."""
    value = bmi(weight_kg, height_m)
    return f"BMI {value:.1f} ({bmi_category(value)})"


if __name__ == "__main__":
    print(bmi(70, 1.75))
    print(bmi_report(70, 1.75))   # BMI 22.9 (normal)
