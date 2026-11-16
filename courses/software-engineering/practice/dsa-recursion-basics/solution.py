def flatten(nested: list) -> list:
    """One flat list of every non-list value, in order."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def power(base: int, exp: int) -> int:
    """base ** exp in O(log exp) steps, without ** or pow."""
    if exp == 0:
        return 1
    half = power(base, exp // 2)
    if exp % 2 == 0:
        return half * half
    return half * half * base


def count_paths(rows: int, cols: int) -> int:
    """Number of right/down paths from top-left to bottom-right of a rows x cols grid."""
    if rows == 1 or cols == 1:
        return 1
    return count_paths(rows - 1, cols) + count_paths(rows, cols - 1)
