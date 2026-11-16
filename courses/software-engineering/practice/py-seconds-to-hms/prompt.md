# Seconds to hours, minutes and seconds

A timer counts seconds, but people want to read `01:02:03`. Use whole-number division `//` and remainder `%` to convert.

```python
def seconds_to_hms(seconds: int) -> str: ...
```

- `seconds` is a whole number, 0 or more.
- Return `"HH:MM:SS"`, each part at least two digits with a leading zero (`f"{x:02d}"`).
- Hours don't wrap at 24: 100 hours is `"100:00:00"`.

**Hint:** there are 3600 seconds in an hour. `seconds // 3600` is the hours; `seconds % 3600` is what's left over. Do the same with 60 for minutes.

## Example

```python
seconds_to_hms(3723)    # "01:02:03"
seconds_to_hms(59)      # "00:00:59"
seconds_to_hms(0)       # "00:00:00"
```
