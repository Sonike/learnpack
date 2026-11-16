from collections import deque


class RecentCounter:
    def __init__(self, window: int):
        self.window = window
        self.times = deque()

    def ping(self, t: int) -> int:
        """Record a request at time t; return how many fall in [t - window, t]."""
        self.times.append(t)
        while self.times[0] < t - self.window:
            self.times.popleft()
        return len(self.times)
