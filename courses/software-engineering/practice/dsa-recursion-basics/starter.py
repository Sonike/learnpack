def flatten(nested: list) -> list:
    """One flat list of every non-list value, in order."""
    result = []
    # TODO: for item in nested: if it's a list, extend result with flatten(item); else append item
    return result


def power(base: int, exp: int) -> int:
    """base ** exp in O(log exp) steps, without ** or pow."""
    # TODO: base case: exp == 0 -> 1
    # TODO: half = power(base, exp // 2); return half * half (times base if exp is odd)
    return 1


def count_paths(rows: int, cols: int) -> int:
    """Number of right/down paths from top-left to bottom-right of a rows x cols grid."""
    # TODO: base case: rows == 1 or cols == 1 -> 1
    # TODO: recursive case: count_paths(rows - 1, cols) + count_paths(rows, cols - 1)
    return 1


if __name__ == "__main__":
    print(flatten([1, [2, [3, 4]], [], 5]))  # want [1, 2, 3, 4, 5]
    print(power(2, 10))                      # want 1024
    print(count_paths(3, 3))                 # want 6
