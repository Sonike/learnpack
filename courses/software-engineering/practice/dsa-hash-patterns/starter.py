from collections import Counter


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Indexes (i, j), i < j, with nums[i] + nums[j] == target, or None. O(n)."""
    index_of = {}  # value -> index where we saw it
    # TODO: for j, number in enumerate(nums):
    #         if target - number is in index_of, return (index_of[target - number], j)
    #         remember index_of[number] = j
    return None


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams, keeping first-seen order."""
    groups = {}  # sorted letters -> list of words
    # TODO: key = "".join(sorted(word)); add word to groups[key] (use setdefault)
    return list(groups.values())


def first_unique_char(s: str) -> int:
    """Index of the first character that appears exactly once, or -1."""
    counts = Counter(s)
    # TODO: scan s with enumerate; return the first index whose count is 1
    return -1


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))  # want (0, 1)
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    print(first_unique_char("loveleetcode"))  # want 2
