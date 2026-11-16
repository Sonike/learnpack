def has_duplicate_quadratic(items: list) -> tuple[bool, int]:
    """Check every pair (i < j). Count 1 step per comparison. Return (answer, steps)."""
    steps = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            steps += 1
            if items[i] == items[j]:
                return True, steps
    return False, steps


def has_duplicate_linear(items: list) -> tuple[bool, int]:
    """Walk the list once with a set of seen values. Count 1 step per item. Return (answer, steps)."""
    steps = 0
    seen = set()
    for item in items:
        steps += 1
        if item in seen:
            return True, steps
        seen.add(item)
    return False, steps


if __name__ == "__main__":
    for n in [100, 200, 400]:
        items = list(range(n))
        print(n, has_duplicate_quadratic(items)[1], has_duplicate_linear(items)[1])
