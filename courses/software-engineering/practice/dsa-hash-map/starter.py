class HashMap:
    def __init__(self, capacity: int = 8):
        self.buckets = [[] for _ in range(capacity)]  # each bucket: a list of [key, value] pairs
        self.size = 0

    def _bucket(self, key) -> list:
        """The bucket (a list) where this key belongs."""
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value) -> None:
        # TODO: look through self._bucket(key); if a pair has this key, replace its value and return
        # TODO: otherwise append [key, value], add 1 to self.size
        # TODO: if self.size / len(self.buckets) > 0.75, call self._resize()
        pass

    def get(self, key, default=None):
        # TODO: return the value for key, or default
        return default

    def remove(self, key) -> bool:
        # TODO: find the pair, delete it from its bucket, subtract 1 from self.size, return True
        return False

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        # TODO: keep the old buckets, make 2x as many empty ones, re-insert every pair
        pass


if __name__ == "__main__":
    m = HashMap()
    m.put("apple", 3)
    m.put("pear", 5)
    m.put("apple", 4)
    print(m.get("apple"), m.get("kiwi", 0), len(m))  # want 4 0 2
    for i in range(10):
        m.put(f"key{i}", i)
    print(len(m), len(m.buckets))  # want 12 32
