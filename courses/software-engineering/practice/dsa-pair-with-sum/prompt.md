# Pair with a target sum (two pointers)

You get a list of numbers **sorted from smallest to largest** and a target. Find two different positions whose values add up to the target.

```python
def pair_with_sum(sorted_nums: list[int], target: int) -> tuple[int, int] | None: ...
```

- `sorted_nums`: integers in ascending order (duplicates allowed).
- `target`: the sum you're looking for.
- Return a tuple of two **indexes** `(i, j)` with `i < j` and `sorted_nums[i] + sorted_nums[j] == target`. If several pairs work, any one is fine. If none works, return `None`.

**It must be O(n).** Use two pointers: `left` starts at the first index, `right` at the last. Look at the sum of the two values:

- too small → move `left` one step right (to a bigger value)
- too big → move `right` one step left (to a smaller value)
- equal → done

Stop when the pointers meet.

## Example

```python
pair_with_sum([1, 3, 4, 6, 9], 10)   # (0, 4)   1 + 9
pair_with_sum([1, 3, 4, 6, 9], 7)    # (0, 3)   1 + 6  ((1, 2), 3 + 4, would also be accepted)
pair_with_sum([1, 3, 4, 6, 9], 100)  # None
```

> **Note:** One test hands you a list of 100,000 numbers that counts how many times you read from it. A nested loop reads billions of times and fails; two pointers reads about 200,000 times and passes.
