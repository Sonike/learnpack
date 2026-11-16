# Rewrite loops as comprehensions

Each function below is described by the loop someone would write first. Write each one as a **single comprehension** instead: a list, dict or set comprehension. The tests only check the results, so the point is practice: get used to reading and writing `[expression for item in items if condition]`.

```python
def squares_of_evens(nums: list[int]) -> list[int]:
def word_lengths(words: list[str]) -> dict[str, int]:
def initials(names: list[str]) -> set[str]:
def flatten(grid: list[list]) -> list:
```

| Function | The loop version | Example |
|---|---|---|
| `squares_of_evens` | for each `n` in `nums`, if `n` is even, append `n * n` | `[1, 2, 3, 4]` → `[4, 16]` |
| `word_lengths` | for each word, `result[word] = len(word)` | `["hi", "there"]` → `{"hi": 2, "there": 5}` |
| `initials` | for each non-empty name, add its first letter in upper case to a set | `["ada", "Alan", "grace", ""]` → `{"A", "G"}` |
| `flatten` | for each row in `grid`, for each item in the row, append the item | `[[1, 2], [3], []]` → `[1, 2, 3]` |

For `flatten`, the `for` clauses go in the same order as the nested loops: `[item for row in grid for item in row]`.
