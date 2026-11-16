def pair_with_sum(sorted_nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indexes (i, j), i < j, whose values sum to target, or None. O(n)."""
    left, right = 0, len(sorted_nums) - 1
    while left < right:
        total = sorted_nums[left] + sorted_nums[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1
        else:
            right -= 1
    return None
