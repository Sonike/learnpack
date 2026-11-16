# Binary search and lower bound

Write binary search yourself, then the variant that the `bisect` module calls `bisect_left`. Both run in O(log n). **Don't import `bisect`** (the tests use it to check you).

## 1. Find a value

```python
def binary_search(nums: list[int], target: int) -> int: ...
```

- `nums`: integers sorted ascending.
- Return an index `i` where `nums[i] == target`, or `-1` if `target` isn't there. (With duplicates, any matching index is fine.)

```python
binary_search([1, 3, 5, 7, 9, 11], 7)  # 3
binary_search([1, 3, 5, 7, 9, 11], 4)  # -1
binary_search([], 4)                   # -1
```

Use `lo = 0`, `hi = len(nums) - 1` and loop `while lo <= hi`. Look at `mid = (lo + hi) // 2`; if it's too small, the answer is right of `mid` (`lo = mid + 1`); if too big, left of it (`hi = mid - 1`).

## 2. Lower bound

```python
def lower_bound(nums: list[int], target: int) -> int: ...
```

Return the **first** index `i` where `nums[i] >= target`. If every value is smaller, return `len(nums)`. This is where you'd insert `target` to keep the list sorted, before any equal values.

```python
lower_bound([1, 3, 3, 3, 8], 3)  # 1
lower_bound([1, 3, 3, 3, 8], 4)  # 4
lower_bound([1, 3, 3, 3, 8], 9)  # 5
lower_bound([1, 3, 3, 3, 8], 0)  # 0
```

Here use `lo = 0`, `hi = len(nums)` and loop `while lo < hi`. If `nums[mid] < target`, the answer is after `mid` (`lo = mid + 1`); otherwise `mid` might be the answer, so keep it (`hi = mid`). When the loop ends, `lo` is the answer.
