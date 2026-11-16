# Sliding windows

Two classic sliding-window problems. In both, a "window" is a stretch of neighbouring items. Instead of rebuilding each window from scratch, you slide it one step and update what changed.

## 1. Biggest sum of `k` neighbours

```python
def max_window_sum(nums: list[int], k: int) -> int | None: ...
```

- `nums`: a list of integers (may include negatives).
- `k`: the window size.
- Return the largest sum of any `k` consecutive numbers. If `k` is less than 1 or bigger than `len(nums)`, return `None`.
- Aim for O(n): sum the first window once, then for each step add the number entering and subtract the one leaving.

```python
max_window_sum([2, 1, 5, 1, 3, 2], 3)  # 9   (5 + 1 + 3)
max_window_sum([-3, -1, -2], 2)        # -3  (-1 + -2)
max_window_sum([1, 2], 5)              # None
```

## 2. Longest stretch with no repeated letter

```python
def longest_unique_substring(s: str) -> int: ...
```

- `s`: any string.
- Return the **length** of the longest substring (neighbouring characters) in which no character appears twice.
- Aim for O(n): keep a `left` edge and a dict `last_seen` of each character's latest index. When the character at `right` was seen inside the current window, jump `left` to just past that earlier position.

```python
longest_unique_substring("abcabcbb")  # 3  ("abc")
longest_unique_substring("pwwkew")    # 3  ("wke")
longest_unique_substring("")          # 0
```
