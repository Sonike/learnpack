# Days until a date

Countdown timers, "due in 3 days" labels and subscription renewals all need the number of days between two dates. The `datetime` module does the calendar maths (month lengths, leap years) for you.

```python
def days_until(date_str: str, today: date) -> int:
```

- `date_str` is a date in ISO format, `"YYYY-MM-DD"`, e.g. `"2026-12-25"`.
- `today` is a `datetime.date`. It's passed in rather than read from the clock so your function gives the same answer every time it's tested. In real code you'd call `days_until(s, date.today())`.
- Return how many days from `today` to that date: `0` if it's today, negative if it's in the past.
- If `date_str` isn't a valid date, let `date.fromisoformat` raise its `ValueError` (don't catch it).

## Example

```python
from datetime import date
days_until("2026-12-25", date(2026, 11, 13))   # 42
days_until("2026-11-10", date(2026, 11, 13))   # -3
```
