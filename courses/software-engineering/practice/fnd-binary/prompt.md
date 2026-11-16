# Convert numbers to and from binary

Computers store every number as a row of bits (0s and 1s). Write the conversion yourself, with a loop, so you see exactly how it works.

```python
def to_binary(n: int) -> str: ...
def from_binary(s: str) -> int: ...
```

- `to_binary(n)` takes a whole number `n` that is 0 or more and returns its binary digits as a string, with no `0b` prefix and no leading zeros. `0` becomes `"0"`.
- `from_binary(s)` takes a string of `0`s and `1`s (leading zeros are allowed) and returns the number it stands for.

**Don't use** `bin()`, `format(n, "b")` or `int(s, 2)`. The tests compare your answers with them, so you can use them in the Run block to check yourself.

**Hints**
- `to_binary`: `n % 2` is the last bit and `n // 2` drops it. Collect bits until `n` is 0, then reverse them.
- `from_binary`: go left to right. For each digit, double the running total and add the digit.

## Example

```python
to_binary(5)          # "101"
to_binary(0)          # "0"
from_binary("1101")   # 13
from_binary("00101")  # 5
```
