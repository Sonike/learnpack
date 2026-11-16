def rotate(items: list, k: int) -> list:
    """Return a new list with items rotated k places to the right."""
    if not items:
        return []
    k = k % len(items)          # now 0 <= k < len(items)
    split = len(items) - k      # where the tail that moves to the front starts
    return items[split:] + items[:split]


if __name__ == "__main__":
    original = [1, 2, 3, 4, 5]
    print(rotate(original, 2))   # [4, 5, 1, 2, 3]
    print(original)              # still [1, 2, 3, 4, 5]
