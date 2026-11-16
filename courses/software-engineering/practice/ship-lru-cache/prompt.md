# An LRU cache, with expiry

Build the cache from the lesson yourself: a fixed-size cache that throws away the **least recently used** entry when it's full. Then add a version where entries expire after a time to live.

## Part 1: `LRUCache`

```python
class LRUCache:
    def __init__(self, capacity: int): ...
    def get(self, key, default=None): ...
    def put(self, key, value) -> None: ...
    def __len__(self) -> int: ...
```

- `capacity`: the most entries the cache may hold. If it's less than 1, raise `ValueError("capacity must be at least 1")`.
- `get(key, default=None)`: return the value stored for `key`, or `default` if it isn't there. A successful `get` makes that key the **most recently used**.
- `put(key, value)`: store the value (replacing any old value). The key becomes the most recently used. If this makes the cache hold more than `capacity` entries, remove the **least recently used** one.
- `len(cache)`: the number of entries currently stored.

`get` and `put` must be O(1): no loops over the entries. Use `collections.OrderedDict`, which remembers insertion order and has `move_to_end(key)` and `popitem(last=False)` (removes the oldest).

## Part 2: `TTLCache`

```python
class TTLCache(LRUCache):
    def __init__(self, capacity: int, ttl: float, now): ...
```

- Same behaviour as `LRUCache`, plus every entry expires `ttl` seconds after it was **put**.
- `now`: a function with no arguments that returns the current time in seconds (in real code you'd pass `time.monotonic`; tests pass a fake clock so they don't have to wait).
- An entry put at time `t` is still valid while `now() < t + ttl`. Once `now() >= t + ttl`, `get` treats it as missing (return `default`) and removes it.
- A `get` doesn't extend the expiry time; only a new `put` does.

## Example

```python
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")       # 1   ("a" is now most recently used)
cache.put("c", 3)    # full: evicts "b", the least recently used
cache.get("b")       # None

clock = [100.0]
ttl = TTLCache(10, ttl=60, now=lambda: clock[0])
ttl.put("rate", 0.92)
clock[0] = 159.9
ttl.get("rate")      # 0.92
clock[0] = 160.0
ttl.get("rate")      # None (expired)
```
