def insertion_sort(items: list, key=None) -> list:
    """Return a new list sorted by key, stable, O(n^2)."""
    key = key or (lambda x: x)
    result = list(items)
    # TODO: for i in range(1, len(result)):
    #         current = result[i]; j = i - 1
    #         while j >= 0 and key(result[j]) > key(current): shift result[j] right, j -= 1
    #         result[j + 1] = current
    return result


def merge_sort(items: list, key=None) -> list:
    """Return a new list sorted by key, stable, O(n log n)."""
    key = key or (lambda x: x)
    # TODO: base case: 0 or 1 items -> return list(items)
    # TODO: split at mid = len(items) // 2, merge_sort both halves (pass key along)
    # TODO: merge: while both halves have items, take the left front if key(left) <= key(right)
    # TODO: then add whatever is left over from either half
    return list(items)


if __name__ == "__main__":
    print(insertion_sort([5, 2, 9, 1]))  # want [1, 2, 5, 9]
    print(merge_sort([5, 2, 9, 1]))      # want [1, 2, 5, 9]
    print(merge_sort([("b", 2), ("a", 1), ("c", 2)], key=lambda t: t[1]))
