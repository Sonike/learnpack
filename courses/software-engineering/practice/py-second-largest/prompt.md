# The second-largest number

```python
def second_largest(nums: list[int]) -> int | None: ...
```

- `nums` is a list of whole numbers, in any order. It may contain duplicates, and it may be short or empty.
- Return the second-largest **distinct** value: in `[5, 5, 3]` the largest is 5 and the second largest is 3, not 5.
- If there is no second distinct value (an empty list, one number, or every number the same), return `None`.
- Don't change the list you were given.

You can solve this in several ways: sort a de-duplicated copy, or walk the list once keeping the best two values seen so far. The one-pass version is a classic interview question; try it after you have a version that works.

## Example

```python
second_largest([3, 9, 4, 9, 1])   # 4
second_largest([-2, -8, -5])      # -5
second_largest([7, 7])            # None
second_largest([])                # None
```
