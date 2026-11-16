import math

from solution import bmi, bmi_category, bmi_report


def test_bmi_formula():
    got = bmi(70, 1.75)
    assert math.isclose(got, 22.857142857142858), f"expected about 22.857, got {got!r}"


def test_bmi_is_not_rounded():
    got = bmi(80, 1.8)
    assert math.isclose(got, 24.691358024691358), f"expected about 24.6914 (unrounded), got {got!r}"


def test_category_boundaries():
    cases = [(18.4, "underweight"), (18.5, "normal"), (24.9, "normal"),
             (25, "overweight"), (29.9, "overweight"), (30, "obese")]
    for value, want in cases:
        got = bmi_category(value)
        assert got == want, f"bmi_category({value}): expected {want!r}, got {got!r}"


def test_report_combines_both_functions():
    got = bmi_report(70, 1.75)
    assert got == "BMI 22.9 (normal)", f"expected 'BMI 22.9 (normal)', got {got!r}"


def test_report_for_other_categories():
    for w, h, want in [(50, 1.8, "BMI 15.4 (underweight)"), (100, 1.7, "BMI 34.6 (obese)")]:
        got = bmi_report(w, h)
        assert got == want, f"bmi_report({w}, {h}): expected {want!r}, got {got!r}"
