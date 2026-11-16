# Insertion sort and merge sort

Write two sorting algorithms by hand: one O(n²) and one O(n log n). **Don't call `sorted` or `.sort()`** (the tests use them to check you).

```python
def insertion_sort(items: list, key=None) -> list: ...
def merge_sort(items: list, key=None) -> list: ...
```

- `items`: the values to sort. **Don't change it**; return a new sorted list.
- `key`: optional function, as in `sorted(items, key=...)`. Compare `key(a)` and `key(b)` instead of `a` and `b`. If `key` is `None`, compare the items themselves (tip: `key = key or (lambda x: x)`).
- Both must be **stable**: items whose keys are equal stay in their original order.

**Insertion sort.** Copy the list. For each position `i` from 1 on, take the item there and slide it left past every item whose key is **bigger** (strictly bigger, which keeps it stable), then drop it in the gap.

**Merge sort.** A list of 0 or 1 items is already sorted. Otherwise split it in half, `merge_sort` each half, then merge the two sorted halves: repeatedly take the smaller front item. When the fronts are equal, take from the **left** half first (which keeps it stable).

## Example

```python
insertion_sort([5, 2, 9, 1])              # [1, 2, 5, 9]
merge_sort(["pear", "fig", "apple"], key=len)
# ["fig", "pear", "apple"]   lengths 3, 4, 5
merge_sort([("b", 2), ("a", 1), ("c", 2)], key=lambda t: t[1])
# [("a", 1), ("b", 2), ("c", 2)]   "b" stays before "c": stable
```
