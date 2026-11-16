from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        # TODO: reject capacity < 1 with ValueError
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key, default=None):
        """Return the value for key (and mark it recently used), or default."""
        # TODO
        return default

    def put(self, key, value) -> None:
        """Store value; evict the least recently used entry if over capacity."""
        # TODO: store, move_to_end, popitem(last=False) when too big
        pass

    def __len__(self) -> int:
        return len(self.data)


class TTLCache(LRUCache):
    def __init__(self, capacity: int, ttl: float, now):
        super().__init__(capacity)
        self.ttl = ttl
        self.now = now

    # TODO: override put to store (value, expires_at)
    # TODO: override get to return default (and delete) once now() >= expires_at


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    print(cache.get("a"))   # 1
    cache.put("c", 3)
    print(cache.get("b"))   # None

    clock = [100.0]
    ttl = TTLCache(10, ttl=60, now=lambda: clock[0])
    ttl.put("rate", 0.92)
    clock[0] = 160.0
    print(ttl.get("rate"))  # None
