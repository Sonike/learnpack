from collections import Counter


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Indexes (i, j), i < j, with nums[i] + nums[j] == target, or None. O(n)."""
    index_of = {}  # value -> index where we saw it
    for j, number in enumerate(nums):
        partner = target - number
        if partner in index_of:
            return (index_of[partner], j)
        index_of[number] = j
    return None


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams, keeping first-seen order."""
    groups = {}  # sorted letters -> list of words
    for word in words:
        groups.setdefault("".join(sorted(word)), []).append(word)
    return list(groups.values())


def first_unique_char(s: str) -> int:
    """Index of the first character that appears exactly once, or -1."""
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
