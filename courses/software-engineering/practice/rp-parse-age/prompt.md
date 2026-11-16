# Validate an age at the boundary

Text typed by a user is untrusted. Turn it into a clean `int` the moment it enters your program, or refuse it loudly with a message that says what was wrong.

```python
def parse_age(s: str) -> int:
```

- `s` is the raw text a user typed, e.g. `"42"` or `" 7 "`.
- Strip surrounding whitespace, then convert to an `int`.
- If it isn't a whole number (`"abc"`, `"4.5"`, `""`), raise `ValueError` with a message that **contains the original text in quotes**, for example `age must be a whole number, got 'abc'`. Use `raise ... from None` so the user doesn't also see `int()`'s own error.
- If the number is below `0` or above `150`, raise `ValueError` with a message that contains `between 0 and 150`, for example `age must be between 0 and 150, got 200`.

## Example

```python
parse_age(" 42 ")   # 42
parse_age("0")      # 0
parse_age("abc")    # ValueError: age must be a whole number, got 'abc'
parse_age("-1")     # ValueError: age must be between 0 and 150, got -1
```
