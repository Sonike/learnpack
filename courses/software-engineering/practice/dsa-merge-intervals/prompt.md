# Merge overlapping intervals

A calendar has bookings as `(start, end)` pairs. Combine every set of bookings that overlap into one.

```python
def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]: ...
```

- `intervals`: `(start, end)` tuples with `start <= end`, in **any** order.
- Return the merged intervals as tuples, sorted by start.
- Intervals that only **touch** (one ends where the next starts, like `(1, 3)` and `(3, 5)`) count as overlapping.
- Don't change the input list.

**The idea:** sorting first makes this easy. After sorting by start, an interval can only overlap the **last** merged one. So walk the sorted list: if the current start is `<=` the last merged end, stretch that end to `max(last_end, current_end)`; otherwise start a new merged interval.

## Example

```python
merge_intervals([(8, 10), (1, 3), (2, 6), (15, 18)])  # [(1, 6), (8, 10), (15, 18)]
merge_intervals([(1, 4), (4, 5)])                     # [(1, 5)]
merge_intervals([(1, 10), (2, 3)])                    # [(1, 10)]
merge_intervals([])                                   # []
```

Sorting is O(n log n) and the walk is O(n), so the whole thing is O(n log n). Use `sorted` here: this exercise is about sorting as a first step, not writing the sort.
