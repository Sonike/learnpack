import heapq


def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    """Return the minimum number of rooms so no overlapping meetings share one."""
    # TODO: sort by start; use a heap of end times for rooms in use
    return 0


if __name__ == "__main__":
    print(min_meeting_rooms([(0, 30), (5, 10), (15, 20)]))  # expected 2
    print(min_meeting_rooms([(1, 5), (5, 9)]))              # expected 1
