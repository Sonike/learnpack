# Rotate a list without changing it

```python
def rotate(items: list, k: int) -> list: ...
```

- `items` is any list.
- `k` is how many places to rotate **to the right**: the last `k` items move to the front.
- `k` may be larger than the list (rotating a 5-item list by 7 is the same as by 2), or negative (rotate to the left).
- Return a **new** list. The caller's `items` must be exactly as it was. The tests check this.
- An empty list returns an empty list.

**Hint:** slicing always makes a new list. `k % len(items)` brings any `k` into range (and makes negative `k` work too), but think about what `% 0` does first.

## Example

```python
rotate([1, 2, 3, 4, 5], 2)    # [4, 5, 1, 2, 3]
rotate([1, 2, 3, 4, 5], 7)    # [4, 5, 1, 2, 3]
rotate([1, 2, 3, 4, 5], -1)   # [2, 3, 4, 5, 1]
rotate([], 3)                 # []
```
