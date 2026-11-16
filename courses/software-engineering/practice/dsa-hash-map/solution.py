class HashMap:
    def __init__(self, capacity: int = 8):
        self.buckets = [[] for _ in range(capacity)]  # each bucket: a list of [key, value] pairs
        self.size = 0

    def _bucket(self, key) -> list:
        """The bucket (a list) where this key belongs."""
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.size += 1
        if self.size / len(self.buckets) > 0.75:
            self._resize()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key) -> bool:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old = self.buckets
        self.buckets = [[] for _ in range(len(old) * 2)]
        for bucket in old:
            for key, value in bucket:
                self._bucket(key).append([key, value])
