# Is it a leap year?

The calendar rule has three parts, and each one is an exception to the one before:

1. A year divisible by **4** is a leap year…
2. …except a year divisible by **100** is not…
3. …except a year divisible by **400** is.

So 2024 is a leap year, 1900 and 2100 are not, and 2000 is.

```python
def is_leap_year(year: int) -> bool: ...
```

- `year` is a positive whole number.
- Return `True` for a leap year, `False` otherwise.

"Divisible by 4" in Python is `year % 4 == 0` (the remainder is zero). You can write this with `if`/`elif`/`else`, or as a single boolean expression with `and`/`or`; try both.

## Example

```python
is_leap_year(2024)   # True
is_leap_year(1900)   # False
is_leap_year(2000)   # True
```
