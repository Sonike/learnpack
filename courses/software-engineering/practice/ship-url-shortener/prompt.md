# A URL shortener

Build the core of the URL shortener from the lesson: each new URL gets the next number from a counter, and the number is written in **base62** to make a short code. Different numbers always give different codes, so there are never collisions.

```python
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(n: int) -> str: ...
def decode(code: str) -> int: ...

class URLShortener:
    def __init__(self): ...
    def shorten(self, url: str) -> str: ...
    def expand(self, code: str) -> str | None: ...
```

- `encode(n)`: write the whole number `n` (0 or more) in base62 using `ALPHABET`, where `ALPHABET[i]` is the digit for value `i`. `encode(0)` is `"0"`. A negative `n` raises `ValueError("n must be 0 or more")`.
- `decode(code)`: the reverse, so `decode(encode(n)) == n`. A character not in `ALPHABET` (or an empty code) raises `ValueError(f"invalid code: {code!r}")`.
- `URLShortener()`: starts with an empty store; the first ID handed out is `1`.
- `shorten(url)`: if this exact URL was shortened before, return the same code. Otherwise take the next ID, store the URL under it, and return `encode(id)`.
- `expand(code)`: return the original URL, or `None` if the code is unknown or invalid.

> **Note:** a real service stores the links in a database and uses the table's auto-increment ID as the counter. Plain dicts are enough here.

## Example

```python
encode(61)     # 'Z'
encode(62)     # '10'
decode("21")   # 125

s = URLShortener()
s.shorten("https://example.com/a")    # '1'
s.shorten("https://example.com/b")    # '2'
s.shorten("https://example.com/a")    # '1'  (same URL, same code)
s.expand("2")                         # 'https://example.com/b'
s.expand("zz")                        # None
```
