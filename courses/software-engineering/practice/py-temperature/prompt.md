# Convert and format temperatures

Two small functions: one does the maths, one turns the result into text for a person to read.

```python
def celsius_to_fahrenheit(c: float) -> float: ...
def format_temp(c: float) -> str: ...
```

- `celsius_to_fahrenheit(c)` takes a temperature in degrees Celsius and returns it in Fahrenheit, using `F = C × 9 / 5 + 32`.
- `format_temp(c)` returns a line like `"21.5°C = 70.7°F"`: both numbers with **exactly one decimal place**. Use an f-string with `:.1f`, and call your first function rather than repeating the formula.

## Example

```python
celsius_to_fahrenheit(100)   # 212.0
celsius_to_fahrenheit(-40)   # -40.0
format_temp(21.5)            # "21.5°C = 70.7°F"
format_temp(0)               # "0.0°C = 32.0°F"
```
