def binary_search(nums: list[int], target: int) -> int:
    """Index of target in sorted nums, or -1."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(nums: list[int], target: int) -> int:
    """First index i with nums[i] >= target (len(nums) if none)."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
