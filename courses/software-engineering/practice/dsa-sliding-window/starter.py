def max_window_sum(nums: list[int], k: int) -> int | None:
    """Largest sum of k consecutive numbers, or None if k < 1 or k > len(nums)."""
    # TODO: handle the None cases
    # TODO: window = sum(nums[:k]); best = window
    # TODO: for i in range(k, len(nums)): add nums[i], subtract nums[i - k], update best
    return None


def longest_unique_substring(s: str) -> int:
    """Length of the longest substring with no repeated character."""
    last_seen = {}
    left = 0
    best = 0
    # TODO: for right, ch in enumerate(s):
    #         if ch in last_seen and last_seen[ch] >= left: left = last_seen[ch] + 1
    #         last_seen[ch] = right
    #         best = max(best, right - left + 1)
    return best


if __name__ == "__main__":
    print(max_window_sum([2, 1, 5, 1, 3, 2], 3))  # want 9
    print(longest_unique_substring("abcabcbb"))   # want 3
    print(longest_unique_substring("pwwkew"))     # want 3
