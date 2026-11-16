def has_duplicate_quadratic(items: list) -> tuple[bool, int]:
    """Check every pair (i < j). Count 1 step per comparison. Return (answer, steps)."""
    steps = 0
    # TODO: loop i over every index, and j over every index after i
    # TODO: add 1 to steps for each comparison; return (True, steps) on a match
    return False, steps


def has_duplicate_linear(items: list) -> tuple[bool, int]:
    """Walk the list once with a set of seen values. Count 1 step per item. Return (answer, steps)."""
    steps = 0
    seen = set()
    # TODO: for each item: add 1 to steps; if it's in seen, return (True, steps); else add it to seen
    return False, steps


if __name__ == "__main__":
    print(has_duplicate_quadratic([3, 1, 4, 1]))  # want (True, 5)
    print(has_duplicate_linear([3, 1, 4, 1]))     # want (True, 4)
    for n in [100, 200, 400]:
        items = list(range(n))  # no duplicates: the worst case
        _, quad = has_duplicate_quadratic(items)
        _, lin = has_duplicate_linear(items)
        print(f"n={n:>4}  quadratic steps={quad:>6}  linear steps={lin:>4}")
