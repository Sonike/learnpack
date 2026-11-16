from collections import deque


class RecentCounter:
    def __init__(self, window: int):
        self.window = window
        self.times = deque()

    def ping(self, t: int) -> int:
        """Record a request at time t; return how many fall in [t - window, t]."""
        # TODO: append t to self.times
        # TODO: while the oldest time (self.times[0]) is < t - self.window: popleft it
        # TODO: return len(self.times)
        return 0


if __name__ == "__main__":
    c = RecentCounter(3000)
    print([c.ping(t) for t in [1, 100, 3001, 3002]])  # want [1, 2, 3, 3]
