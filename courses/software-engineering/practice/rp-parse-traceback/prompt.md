# Read a traceback with code

When Python crashes it prints a **traceback**. The useful facts are at the bottom: the exception type, its message, and the innermost frame (the last `File "...", line N, in ...` line), which is where the error actually happened.

Write a function that pulls those four facts out of a traceback string.

```python
def parse_traceback(text: str) -> dict:
```

- `text` is a whole traceback exactly as Python printed it, including the `Traceback (most recent call last):` header.
- Return a dict with four keys:
  - `"type"`: the exception name, e.g. `"KeyError"` (keep any dotted prefix, e.g. `"json.decoder.JSONDecodeError"`).
  - `"message"`: everything after the first `": "` on the last line, or `""` if the last line has no message (e.g. `KeyboardInterrupt`).
  - `"file"`: the file name from the **last** `File "..."` line.
  - `"line"`: that frame's line number, as an `int`.
- Ignore blank lines at the end. If there are several tracebacks chained together ("During handling of the above exception..."), the last one is the one that crashed the program, so the last `File` line and the last line win.

## Example

```python
text = '''Traceback (most recent call last):
  File "shop.py", line 12, in <module>
    print(total(cart))
  File "shop.py", line 5, in total
    return prices[item] * qty
           ~~~~~~^^^^^^
KeyError: 'banana'
'''
parse_traceback(text)
# {"type": "KeyError", "message": "'banana'", "file": "shop.py", "line": 5}
```

Hint: `text.strip().splitlines()`, `line.strip().startswith('File "')`, and `str.partition(": ")` do most of the work.
