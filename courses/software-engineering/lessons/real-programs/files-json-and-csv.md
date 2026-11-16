# Files, JSON and CSV

Everything your program knows disappears when it stops, unless you save it somewhere. Files are the simplest place: settings, exports from a spreadsheet, logs, data downloaded from an API. Most real-world scripts boil down to "read a file, do something with the data, write a file", and two formats, **CSV** and **JSON**, cover most of the data you'll meet.

## Opening, reading and writing

`open` gives you a **file object**, a handle you read from or write to. Always open files with a `with` statement:

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("first line\n")
    f.write("second line\n")

with open("notes.txt", encoding="utf-8") as f:
    text = f.read()

print(text)
# first line
# second line
```

Three things are going on here.

**The mode** (the second argument) says what you want to do:

| Mode | Meaning | If the file exists | If it doesn't |
|---|---|---|---|
| `"r"` (default) | read | read it | `FileNotFoundError` |
| `"w"` | write | **erase it** and start empty | create it |
| `"a"` | append | add to the end | create it |
| `"x"` | create | `FileExistsError` | create it |

Be careful with `"w"`: it empties the file the moment it opens, before you write anything.

**The encoding.** Files store bytes; text is characters. An **encoding** is the rule that turns one into the other. **UTF-8** handles every language and emoji and is the standard almost everywhere. If you leave `encoding` out, Python uses your operating system's default, which on some Windows setups isn't UTF-8, so a file with "Zoë" or "₦" in it reads fine on your laptop and crashes (or turns into garbage) on someone else's. Always write `encoding="utf-8"`.

**The `with` statement** closes the file for you when the block ends, **even if an exception happens inside it**. An open file holds resources; written data may sit in a memory buffer and not reach the disk until the file is closed. Without `with`, you'd need this:

```python
f = open("notes.txt", encoding="utf-8")
try:
    text = f.read()
finally:
    f.close()
```

`with` is that pattern in one line. Use it every time.

### Reading line by line

`f.read()` loads the whole file into one string. For big files, loop over the file object instead: it gives you one line at a time without loading everything into memory.

```python
with open("notes.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip("\n"))
# 1 first line
# 2 second line
```

Each line keeps its `\n` at the end, which is why we strip it. Forget that and `print` adds a second newline, giving you double-spaced output.

## Paths with pathlib

A **path** is a file's address: `notes.txt` (relative to the folder your program runs in, the **current working directory**) or `/home/ada/projects/notes.txt` (absolute). The `pathlib` module turns paths into objects with useful methods, and joins them correctly on every operating system (Windows uses `\`, macOS and Linux use `/`).

```python
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)          # create the folder if it's missing

report = data_dir / "report.txt"       # "/" joins path parts
report.write_text("all good\n", encoding="utf-8")

print(report)                  # data/report.txt
print(report.exists())         # True
print(report.name)             # report.txt
print(report.suffix)           # .txt
print(report.stem)             # report
print(report.read_text(encoding="utf-8"))   # all good

for path in data_dir.glob("*.txt"):          # every .txt file in data/
    print(path.name)
# report.txt
```

`read_text` and `write_text` open, read or write, and close in one call: handy for small files. `open(path)` accepts a `Path` too.

> **Note:** a relative path is relative to where you **run** the program, not where the `.py` file lives. If `python scripts/report.py` can't find `data/input.csv`, check which folder your terminal is in (`pwd`).

## CSV: tables in plain text

**CSV** (comma-separated values) is how spreadsheets export tables. The first line is usually a **header** with column names:

```
name,email,city
Ada,ada@example.com,London
Grace,grace@example.com,New York
```

It looks easy to split each line on commas yourself. Don't: values can contain commas inside quotes (`"12 High St, London"`), quotes inside quotes, and even newlines. The `csv` module handles all of that. `csv.DictReader` gives you each row as a dict keyed by the header:

```python
import csv

with open("contacts.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(row["name"], "lives in", row["city"])
# Ada lives in London
# Grace lives in New York
```

Notice `newline=""`. The `csv` module wants to handle line endings itself (Windows files end lines with `\r\n`), and the docs ask you to open CSV files this way. Also notice that **every value is a string**: `row["age"]` is `"36"`, not `36`. Convert explicitly with `int(...)` or `float(...)`, ideally right where you read the row.

Writing works the same way with `csv.DictWriter`:

```python
import csv

people = [
    {"name": "Ada", "score": 91},
    {"name": "Grace", "score": 85},
]

with open("scores.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerows(people)
```

`scores.csv` now contains:

```
name,score
Ada,91
Grace,85
```

## JSON: nested data

CSV is great for flat tables. For anything nested (a user with a list of addresses, a settings file with sections) the standard is **JSON** (JavaScript Object Notation). It's also what nearly every web API sends and receives, so you'll use it constantly in the web section.

JSON looks almost exactly like Python dicts and lists:

```json
{
  "theme": "dark",
  "font_size": 14,
  "recent_files": ["notes.txt", "todo.md"],
  "autosave": true,
  "backup_folder": null
}
```

The differences: JSON strings always use double quotes, and `true`/`false`/`null` are lowercase (Python's `True`/`False`/`None`).

The `json` module converts between the two. `json.dump` writes Python data to a file; `json.load` reads it back:

```python
import json

settings = {"theme": "dark", "font_size": 14, "recent_files": ["notes.txt"]}

with open("settings.json", "w", encoding="utf-8") as f:
    json.dump(settings, f, indent=2)

with open("settings.json", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded == settings)    # True
print(loaded["recent_files"][0])   # notes.txt
```

`indent=2` makes the file readable by humans. Two more options you'll want: `ensure_ascii=False` keeps characters like `ë` as they are instead of writing `ë`, and `sort_keys=True` gives stable output that's easy to compare.

The functions with an **s** on the end, `json.dumps` and `json.loads`, work with strings instead of files ("dump string", "load string"):

```python
import json

text = json.dumps({"ok": True, "items": [1, 2]})
print(text)                   # {"ok": true, "items": [1, 2]}
print(json.loads(text)["items"])   # [1, 2]
```

Not everything can be turned into JSON. Sets, dates and your own objects raise `TypeError: Object of type set is not JSON serializable`. Convert them first: a set to a list, a date to an ISO string like `"2026-11-13"`.

## When files go wrong

Files live outside your program, so they fail in ways your code can't prevent: the file doesn't exist yet, the user doesn't have permission, someone edited the JSON by hand and left a comma dangling. Decide what each failure should mean, and handle the ones you can (the lesson "Handling exceptions" covers the tools).

```python
import json

DEFAULTS = {"theme": "light", "font_size": 14}

def load_settings(path):
    try:
        with open(path, encoding="utf-8") as f:
            saved = json.load(f)
    except FileNotFoundError:
        return dict(DEFAULTS)                 # first run: no file yet, that's normal
    except json.JSONDecodeError as e:
        print(f"warning: {path} is broken ({e}); using defaults")
        return dict(DEFAULTS)
    return {**DEFAULTS, **saved}
```

A few things worth copying from this:

- A **missing settings file is normal** on first run, so it's handled quietly.
- A **corrupt file** is handled too, but with a warning, because someone probably wants to know.
- `{**DEFAULTS, **saved}` builds a new dict: the defaults first, then the saved values on top. A setting that's new in this version of your app still gets its default.
- It returns `dict(DEFAULTS)`, a **copy**. Returning `DEFAULTS` itself would let the caller accidentally change your defaults for everyone.
- A `PermissionError` isn't caught. There's no sensible fallback, so the program should stop and say so.

## Common mistakes

**Forgetting the encoding.** Works on your machine, breaks on a colleague's: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f`. Add `encoding="utf-8"`.

**Opening with `"w"` when you meant `"a"`.** Your log file now only contains the last line. There's no undo.

**Splitting CSV on commas by hand.** Works until the first address with a comma in it. Use `csv`.

**Treating CSV values as numbers.** `row["price"] * 2` on `"4.50"` gives `"4.504.50"`, no error at all. Convert with `float()`.

**Confusing `load` and `loads`.** `json.loads(f)` gives `TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper`. Use `load` for files, `loads` for strings.

**`FileNotFoundError` for a file that exists.** Almost always the current working directory: your terminal is in a different folder from the one you think. Print `Path.cwd()` and `Path("data.csv").resolve()` to see where Python is really looking.

## Recap

- Open files with `with open(path, mode, encoding="utf-8")`. `with` closes the file even when an exception happens.
- Modes: `"r"` read, `"w"` overwrite, `"a"` append, `"x"` create-only. Loop over a file object to read line by line.
- `pathlib.Path` builds paths with `/`, and has `exists`, `read_text`, `write_text`, `glob`, `name` and `suffix`.
- CSV: `csv.DictReader` and `csv.DictWriter`, open with `newline=""`, and remember every value is a string.
- JSON: `json.load`/`json.dump` for files, `loads`/`dumps` for strings, `indent=2` for humans.
- Decide what a missing or broken file means for your program, and handle exactly those cases.
