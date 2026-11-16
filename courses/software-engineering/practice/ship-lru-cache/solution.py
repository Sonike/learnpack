from collections import OrderedDict

MISSING = object()


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key, default=None):
        """Return the value for key (and mark it recently used), or default."""
        if key not in self.data:
            return default
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value) -> None:
        """Store value; evict the least recently used entry if over capacity."""
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

    def __len__(self) -> int:
        return len(self.data)


class TTLCache(LRUCache):
    def __init__(self, capacity: int, ttl: float, now):
        super().__init__(capacity)
        self.ttl = ttl
        self.now = now

    def put(self, key, value) -> None:
        super().put(key, (value, self.now() + self.ttl))

    def get(self, key, default=None):
        entry = super().get(key, MISSING)
        if entry is MISSING:
            return default
        value, expires_at = entry
        if self.now() >= expires_at:
            del self.data[key]
            return default
        return value
