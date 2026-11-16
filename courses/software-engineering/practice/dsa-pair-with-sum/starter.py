def pair_with_sum(sorted_nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indexes (i, j), i < j, whose values sum to target, or None. O(n)."""
    left, right = 0, len(sorted_nums) - 1
    # TODO: while left < right:
    #         total = sorted_nums[left] + sorted_nums[right]
    #         equal -> return (left, right); too small -> left += 1; too big -> right -= 1
    return None


if __name__ == "__main__":
    print(pair_with_sum([1, 3, 4, 6, 9], 10))   # want (0, 4)
    print(pair_with_sum([1, 3, 4, 6, 9], 7))    # want (0, 3) (or (1, 2))
    print(pair_with_sum([1, 3, 4, 6, 9], 100))  # want None
