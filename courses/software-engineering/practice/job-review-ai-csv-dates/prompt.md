# Review the AI's code: `parse_csv_dates`

A teammate asked a coding assistant for a function and pasted the result into a pull request. It looks fine, it runs, and it returns datetimes. It also has **three bugs**. Your job is the reviewer's job: read every line, find them, fix them.

The starter already contains the AI-written code. Don't rewrite from scratch: fix it, so you practise reading code you didn't write.

## What the function must do

`parse_csv_dates(csv_text: str, column: str) -> list[datetime]`

- `csv_text` is a whole CSV file as a string. Its first line is a header row with column names.
- `column` is the name of the column that holds timestamps in ISO 8601 format, such as `2026-03-01T09:30:00+01:00`.
- Return one `datetime` per data row, in file order, **converted to UTC** (`timezone.utc`). A value like `09:30+01:00` is `08:30` UTC. A value with no offset (like `2026-03-01T09:30:00`) is already UTC; attach `timezone.utc` to it.
- Skip rows where the value is empty.
- If a value isn't a valid timestamp, raise `ValueError` with a message that contains `line N`, where N is the line number in the file (the header is line 1, the first data row is line 2).

## Example

```python
text = """id,created_at
1,2026-03-01T09:30:00+01:00
2,2026-03-01T12:00:00
3,
"""
parse_csv_dates(text, "created_at")
# [datetime(2026, 3, 1, 8, 30, tzinfo=timezone.utc),
#  datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)]
```

> **Hint:** run the example in the starter and compare with the expected output above. Then look closely at three things: how the offset is handled, which rows the loop visits, and what happens to errors.
