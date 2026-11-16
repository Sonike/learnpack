# Range sums with prefix sums

A dashboard asks the same question many times: "what's the total of `nums` from position `left` to position `right`?" Adding up the range every time costs O(n) per question. Build a **prefix sum** list once, then answer each question in O(1).

```python
def range_sum_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]: ...
```

- `nums`: a list of integers.
- `queries`: a list of `(left, right)` index pairs. Both ends are **included**, and `0 <= left <= right < len(nums)`.
- Return a list with one total per query, in the same order.

**The trick.** Make `prefix` one longer than `nums`, where `prefix[i]` is the sum of the first `i` numbers:

```
nums   =    [3,  1,  4,  1,  5]
prefix = [0, 3,  4,  8,  9, 14]
```

Then the sum from `left` to `right` is `prefix[right + 1] - prefix[left]`.

## Example

```python
range_sum_queries([3, 1, 4, 1, 5], [(0, 2), (1, 3), (4, 4)])  # [8, 6, 5]
```

`(0, 2)` is `3 + 1 + 4 = 8`, which is `prefix[3] - prefix[0] = 8 - 0`.
