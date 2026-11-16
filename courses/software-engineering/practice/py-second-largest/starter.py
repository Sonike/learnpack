def second_largest(nums: list[int]) -> int | None:
    """Return the second-largest distinct value in nums, or None if there isn't one."""
    # TODO: remove duplicates (set() helps), sort, and pick the right index,
    #       or loop once and track the largest and second-largest values so far
    return None


if __name__ == "__main__":
    print(second_largest([3, 9, 4, 9, 1]))   # 4
    print(second_largest([7, 7]))            # None
