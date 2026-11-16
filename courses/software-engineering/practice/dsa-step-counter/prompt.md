# Count the steps: quadratic vs linear

Big-O is about how the amount of work **grows** as the input grows. Here you'll measure it yourself. Write two functions that answer the same question, "does this list contain any value twice?", and make each one count its own steps.

```python
def has_duplicate_quadratic(items: list) -> tuple[bool, int]: ...
def has_duplicate_linear(items: list) -> tuple[bool, int]: ...
```

- `items` is a list of hashable values (numbers or strings).
- Both return a **tuple** `(answer, steps)`: `answer` is `True` if some value appears more than once, and `steps` is how much work you did.

**How to count steps**

- `has_duplicate_quadratic`: compare every pair `items[i]` and `items[j]` with `i < j` (a loop inside a loop). Add **1 step for every comparison**. Stop and return as soon as you find a match.
- `has_duplicate_linear`: walk through the list once, keeping a `set` of values you've seen. Add **1 step for every item you look at**. Stop and return as soon as you see a value that's already in the set.

## Example

```python
has_duplicate_quadratic([3, 1, 4, 1])  # (True, 5)   pairs checked: 3-1, 3-4, 3-1, 1-4, 1-1 ✓
has_duplicate_linear([3, 1, 4, 1])     # (True, 4)   looked at 3, 1, 4, 1 ✓
has_duplicate_quadratic([1, 2, 3])     # (False, 3)  3 pairs, no match
has_duplicate_linear([1, 2, 3])        # (False, 3)
```

When the list has no duplicates, the quadratic version does `n × (n − 1) / 2` steps and the linear one does `n`. Double `n` and the first count goes up about **4×**, the second exactly **2×**. Run the starter to see it.
