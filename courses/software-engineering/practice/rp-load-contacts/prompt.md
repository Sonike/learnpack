# Load contacts from a messy CSV

Real CSV files are messy: someone typed spaces after the commas, and there are empty rows where a line was deleted in a spreadsheet. Read the file into a clean list of dicts.

```python
def load_contacts(path) -> list[dict]:
```

- `path` is the location of a CSV file (a `str` or a `pathlib.Path`). The first row is the header, e.g. `name,email,city`.
- Return one dict per contact, with the header names as keys, e.g. `{"name": "Ada", "email": "ada@example.com", "city": "London"}`.
- Strip whitespace from every key and every value.
- Skip rows where every value is blank after stripping (like `,,`).
- Open the file with `encoding="utf-8"` and `newline=""` (the `csv` module asks for this), inside a `with` block, and use `csv.DictReader`.
- If a row is shorter than the header, `DictReader` gives `None` for the missing values: treat those as `""`.

## Example

`contacts.csv`:
```
name, email ,city
 Ada , ada@example.com, London
,,
Grace,grace@example.com,  New York
```

```python
load_contacts("contacts.csv")
# [{"name": "Ada", "email": "ada@example.com", "city": "London"},
#  {"name": "Grace", "email": "grace@example.com", "city": "New York"}]
```
