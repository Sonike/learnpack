def first_bad_version(versions: list[str], is_bad) -> int:
    """Index of the first version where is_bad(version) is True, or -1. Use binary search."""
    low, high = 0, len(versions)
    # The answer is always in the range low..high (high means "nothing bad").
    while low < high:
        mid = (low + high) // 2
        if is_bad(versions[mid]):
            high = mid
        else:
            low = mid + 1
    return low if low < len(versions) else -1
