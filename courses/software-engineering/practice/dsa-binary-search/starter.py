def binary_search(nums: list[int], target: int) -> int:
    """Index of target in sorted nums, or -1."""
    lo, hi = 0, len(nums) - 1
    # TODO: while lo <= hi: mid = (lo + hi) // 2, compare nums[mid] with target, move lo or hi
    return -1


def lower_bound(nums: list[int], target: int) -> int:
    """First index i with nums[i] >= target (len(nums) if none)."""
    lo, hi = 0, len(nums)
    # TODO: while lo < hi: mid = (lo + hi) // 2
    #         nums[mid] < target -> lo = mid + 1, otherwise hi = mid
    return lo


if __name__ == "__main__":
    print(binary_search([1, 3, 5, 7, 9, 11], 7))  # want 3
    print(binary_search([1, 3, 5, 7, 9, 11], 4))  # want -1
    print(lower_bound([1, 3, 3, 3, 8], 3))        # want 1
    print(lower_bound([1, 3, 3, 3, 8], 9))        # want 5
