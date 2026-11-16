# Interview problem: longest consecutive sequence (medium)

> **Note:** 30-minute timer. Say the brute force out loud first (sorting is O(n log n)); the interviewer will then ask for O(n).

Given a list of integers, return the length of the **longest run of consecutive values** (like 4, 5, 6, 7) that can be formed from them. Order in the list doesn't matter, and duplicates count once.

Write `longest_consecutive(nums: list[int]) -> int` that runs in **O(n)** time.

## Examples

```python
longest_consecutive([100, 4, 200, 1, 3, 2])   # 4   (1, 2, 3, 4)
longest_consecutive([0, -1, 1, 2, 9])         # 4   (-1, 0, 1, 2)
longest_consecutive([1, 2, 2, 3])             # 3
longest_consecutive([])                       # 0
```

> **Hint:** put the numbers in a `set` for O(1) lookups. Only start counting from a number `x` when `x - 1` is **not** in the set: then `x` is the start of a run, and each number is visited a constant number of times overall.
