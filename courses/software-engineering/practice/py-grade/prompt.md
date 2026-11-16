# Turn a score into a grade

```python
def grade(score: int) -> str: ...
```

- `score` is an exam score.
- Return the letter grade:

| Score | Grade |
|---|---|
| 90–100 | `"A"` |
| 80–89 | `"B"` |
| 70–79 | `"C"` |
| 60–69 | `"D"` |
| 0–59 | `"F"` |

- A score below 0 or above 100 is a mistake by whoever called the function. Don't guess a grade: **raise an error** with
  ```python
  raise ValueError(f"score must be between 0 and 100, got {score}")
  ```
  `raise` stops the function and reports the problem. You'll learn errors properly later; for now, this one line is all you need.

Watch the **boundaries**: 90 is an A, 89 is a B, 100 is an A, 0 is an F. Bugs live at the edges.

## Example

```python
grade(95)    # "A"
grade(80)    # "B"
grade(59)    # "F"
grade(101)   # raises ValueError
```
