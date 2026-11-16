# Build your own hash map

Build a small version of Python's `dict` so you know what happens inside one. **Don't use a `dict` (or `set`) anywhere in your class.**

```python
class HashMap:
    def __init__(self, capacity: int = 8): ...
    def put(self, key, value) -> None: ...
    def get(self, key, default=None): ...
    def remove(self, key) -> bool: ...
    def __len__(self) -> int: ...
```

**How it's stored.** `self.buckets` is a list of `capacity` buckets, and each bucket is a plain list of `[key, value]` pairs. A key lives in bucket number `hash(key) % len(self.buckets)`. Two keys landing in the same bucket is a **collision**; they simply share that bucket's list (this is called **chaining**).

- `put(key, value)`: if the key is already in its bucket, replace its value. Otherwise add `[key, value]` to the bucket. After adding a **new** key, if `len(self) / len(self.buckets) > 0.75` (the **load factor**), resize: make a bucket list twice as long and put every pair back in (their bucket numbers change, because the `%` is different).
- `get(key, default=None)`: the value for `key`, or `default` if it isn't there.
- `remove(key)`: delete the pair and return `True`; return `False` if the key wasn't there.
- `len(m)`: how many keys are stored.

Compare keys with `==`, as `dict` does.

## Example

```python
m = HashMap()
m.put("apple", 3)
m.put("pear", 5)
m.put("apple", 4)      # replaces, doesn't add
m.get("apple")         # 4
m.get("kiwi", 0)       # 0
len(m)                 # 2
m.remove("pear")       # True
m.remove("pear")       # False
len(m.buckets)         # 8; after the 7th distinct key it becomes 16
```
