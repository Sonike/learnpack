def range_sum_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Answer each (left, right) inclusive range-sum query using prefix sums."""
    prefix = [0]
    # TODO: for each number, append prefix[-1] + number
    # TODO: return [prefix[right + 1] - prefix[left] for each (left, right)]
    return []


if __name__ == "__main__":
    print(range_sum_queries([3, 1, 4, 1, 5], [(0, 2), (1, 3), (4, 4)]))  # want [8, 6, 5]
