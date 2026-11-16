# Count recent requests with a queue

A rate limiter needs to know "how many requests arrived in the last `window` seconds?" Keep the timestamps in a **queue** (first in, first out): new ones join at the back, and old ones fall off the front.

```python
class RecentCounter:
    def __init__(self, window: int): ...
    def ping(self, t: int) -> int: ...
```

- `window`: how many seconds back to count.
- `ping(t)`: a request arrived at time `t` (seconds). Record it, then return how many recorded requests have a time in `[t - window, t]`, **both ends included**. Times passed to `ping` never go backwards.

The time is passed in rather than read from a clock, so your code is easy to test.

Store the timestamps in `self.times`, a `collections.deque` (the starter sets it up; one test checks its length). A deque's `append` adds to the back and `popleft` removes from the front, both O(1). (A list's `pop(0)` is O(n), because every remaining item has to shift left.) Each timestamp is added once and removed at most once, so the average cost per `ping` is O(1).

## Example

```python
c = RecentCounter(3000)
c.ping(1)     # 1   [1]
c.ping(100)   # 2   [1, 100]
c.ping(3001)  # 3   [1, 100, 3001]   1 is exactly 3000 ago: still counts
c.ping(3002)  # 3   [100, 3001, 3002]  1 fell out
```
