def insertion_sort(items: list, key=None) -> list:
    """Return a new list sorted by key, stable, O(n^2)."""
    key = key or (lambda x: x)
    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and key(result[j]) > key(current):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def merge_sort(items: list, key=None) -> list:
    """Return a new list sorted by key, stable, O(n log n)."""
    key = key or (lambda x: x)
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
