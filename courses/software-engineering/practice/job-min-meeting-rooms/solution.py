import heapq


def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    """Return the minimum number of rooms so no overlapping meetings share one."""
    ends = []  # min-heap: end time of each room in use
    most = 0
    for start, end in sorted(intervals):
        while ends and ends[0] <= start:
            heapq.heappop(ends)  # that meeting is over; its room is free
        heapq.heappush(ends, end)
        most = max(most, len(ends))
    return most
