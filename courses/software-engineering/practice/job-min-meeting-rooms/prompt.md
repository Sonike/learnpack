# Interview problem: meeting rooms (medium)

> **Note:** treat this like an interview. Set a 30-minute timer. Clarify, write two examples by hand, say the brute force, then optimise. Don't press Check until you've traced your code on an example yourself.

Given a list of meetings, return the **minimum number of rooms** needed so that no two overlapping meetings share a room.

Write `min_meeting_rooms(intervals: list[tuple[int, int]]) -> int`.

- Each meeting is `(start, end)` with `start < end`, in minutes.
- A meeting occupies its room from `start` up to, but not including, `end`. So a meeting ending at 10 and another starting at 10 **can** use the same room.
- The list may be empty and isn't sorted.

## Examples

```python
min_meeting_rooms([(0, 30), (5, 10), (15, 20)])   # 2
min_meeting_rooms([(7, 10), (2, 4)])              # 1
min_meeting_rooms([(1, 5), (5, 9)])               # 1  (back to back is fine)
min_meeting_rooms([])                             # 0
```

Aim for **O(n log n)** time.

> **Hint:** sort by start time. Keep a min-heap (`heapq`) of end times for rooms in use. Before placing a meeting, free every room whose meeting has ended. The most rooms ever in use at once is the answer.
