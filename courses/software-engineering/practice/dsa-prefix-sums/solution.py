def range_sum_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Answer each (left, right) inclusive range-sum query using prefix sums."""
    prefix = [0]
    for number in nums:
        prefix.append(prefix[-1] + number)
    return [prefix[right + 1] - prefix[left] for left, right in queries]
