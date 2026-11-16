def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping or touching intervals; return them sorted by start."""
    merged: list[list[int]] = []
    # TODO: for start, end in sorted(intervals):
    #         if merged and start <= merged[-1][1]: stretch merged[-1][1] to max(...)
    #         else: merged.append([start, end])
    # TODO: return a list of tuples
    return []


if __name__ == "__main__":
    print(merge_intervals([(8, 10), (1, 3), (2, 6), (15, 18)]))  # want [(1, 6), (8, 10), (15, 18)]
