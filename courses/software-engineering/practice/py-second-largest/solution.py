def second_largest(nums: list[int]) -> int | None:
    """Return the second-largest distinct value in nums, or None if there isn't one."""
    distinct = sorted(set(nums))
    if len(distinct) < 2:
        return None
    return distinct[-2]


if __name__ == "__main__":
    print(second_largest([3, 9, 4, 9, 1]))   # 4
    print(second_largest([7, 7]))            # None
