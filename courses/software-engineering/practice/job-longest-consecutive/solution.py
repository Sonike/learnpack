def longest_consecutive(nums: list[int]) -> int:
    """Length of the longest run of consecutive integers in nums, in O(n)."""
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:
            continue  # not the start of a run
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best
