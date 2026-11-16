def max_window_sum(nums: list[int], k: int) -> int | None:
    """Largest sum of k consecutive numbers, or None if k < 1 or k > len(nums)."""
    if k < 1 or k > len(nums):
        return None
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


def longest_unique_substring(s: str) -> int:
    """Length of the longest substring with no repeated character."""
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
