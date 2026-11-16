def common_friends(a: set[str], b: set[str]) -> list[str]:
    """Return the names in both sets, sorted A-Z."""
    return sorted(a & b)


def unique_in_order(items: list) -> list:
    """Return items without duplicates, keeping first occurrences in order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


if __name__ == "__main__":
    print(common_friends({"ana", "ben", "cy"}, {"cy", "dee", "ana"}))   # ['ana', 'cy']
    print(unique_in_order([3, 1, 3, 2, 1]))                               # [3, 1, 2]
