# Keep going when one item fails

A batch job that crashes on item 3 of 10,000 loses all the work. Often the better move is to handle each item on its own, collect the failures, and report them at the end.

```python
def safe_divide_all(pairs: list[tuple]) -> tuple[list[float], list[str]]:
```

- `pairs` is a list of `(a, b)` tuples. Divide `a / b` for each one.
- Return two lists: `(results, errors)`.
  - `results` holds the answers of the divisions that worked, in order.
  - `errors` holds one string per pair that failed, in the form `"pair 2: division by zero"`: the **index** of the pair in `pairs`, a colon, then the exception's message (`str(e)`).
- Catch only `ZeroDivisionError` and `TypeError` (e.g. `("6", 2)`). Don't catch everything: a bug of another kind should still crash.

## Example

```python
safe_divide_all([(10, 2), (1, 0), ("6", 2), (9, 3)])
# ([5.0, 3.0],
#  ["pair 1: division by zero",
#   "pair 2: unsupported operand type(s) for /: 'str' and 'int'"])
```
