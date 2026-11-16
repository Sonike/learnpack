def first_bad_version(versions: list[str], is_bad) -> int:
    """Index of the first version where is_bad(version) is True, or -1. Use binary search."""
    low, high = 0, len(versions)
    # TODO: while low < high:
    #         mid = (low + high) // 2
    #         if versions[mid] is bad, the answer is mid or earlier  -> high = mid
    #         otherwise the answer is after mid                       -> low = mid + 1
    # TODO: when the loop ends, low is the answer (or len(versions) if nothing was bad)
    return -1


if __name__ == "__main__":
    versions = [f"v{n}" for n in range(1, 101)]
    calls = []

    def is_bad(version):
        calls.append(version)
        return int(version[1:]) >= 58

    print("first bad index:", first_bad_version(versions, is_bad))  # want 57 (that's v58)
    print("checked:", calls)
