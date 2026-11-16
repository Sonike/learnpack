# How many bytes is this text?

Text is stored as numbers. Each character has a **code point** (a number from Unicode), and **UTF-8** turns each code point into 1 to 4 bytes. English letters take 1 byte, `é` takes 2, most Chinese characters take 3 and most emoji take 4.

Write two small functions:

```python
def code_points(text: str) -> list[int]: ...
def utf8_byte_count(text: str) -> int: ...
```

- `code_points(text)` returns the Unicode code point of every character, in order. The built-in `ord(ch)` gives you one character's code point.
- `utf8_byte_count(text)` returns how many bytes `text` takes when encoded as UTF-8. `text.encode("utf-8")` gives you a `bytes` object, and `len()` counts its bytes.

## Example

```python
code_points("Hi!")        # [72, 105, 33]
utf8_byte_count("Hi!")    # 3
utf8_byte_count("café")   # 5   (4 characters, but é takes 2 bytes)
utf8_byte_count("🙂")     # 4
```
