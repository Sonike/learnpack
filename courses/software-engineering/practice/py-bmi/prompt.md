# BMI: small functions that work together

Break a problem into small functions, each doing one job, then combine them.

```python
def bmi(weight_kg: float, height_m: float) -> float: ...
def bmi_category(value: float) -> str: ...
def bmi_report(weight_kg: float, height_m: float) -> str: ...
```

- `bmi(weight_kg, height_m)` returns body-mass index: weight in kilograms divided by height in metres squared (`weight_kg / height_m ** 2`). Don't round it.
- `bmi_category(value)` takes a BMI number and returns:
  - `"underweight"` below 18.5
  - `"normal"` from 18.5 up to (not including) 25
  - `"overweight"` from 25 up to (not including) 30
  - `"obese"` at 30 or above
- `bmi_report(weight_kg, height_m)` **calls the other two** and returns text like `"BMI 22.9 (normal)"`, with the BMI to one decimal place.

## Example

```python
bmi(70, 1.75)            # 22.857142857142858
bmi_category(22.86)      # "normal"
bmi_category(25)         # "overweight"
bmi_report(70, 1.75)     # "BMI 22.9 (normal)"
```
