# Convert a CSV file to JSON

Spreadsheets export CSV; web APIs speak JSON. Converting one to the other is one of the most common small scripts you'll write.

```python
def csv_to_json(csv_path, json_path) -> int:
```

- `csv_path` is an existing CSV file with a header row. `json_path` is where to write the result.
- Read every row with `csv.DictReader` and write them to `json_path` as a JSON **list of objects**, one object per row, in the same order. Values stay strings.
- Use `encoding="utf-8"` for both files (and `newline=""` when reading the CSV). Write with `indent=2` and `ensure_ascii=False` so names like `Zoë` stay readable in the file.
- Return the number of rows written.

## Example

`people.csv`:
```
name,age
Ada,36
Zoë,29
```

```python
csv_to_json("people.csv", "people.json")   # 2
```

`people.json` now holds:
```json
[
  {
    "name": "Ada",
    "age": "36"
  },
  {
    "name": "Zoë",
    "age": "29"
  }
]
```
