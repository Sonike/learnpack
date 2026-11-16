def rotate(items: list, k: int) -> list:
    """Return a new list with items rotated k places to the right."""
    # TODO: an empty list has nothing to rotate (and % 0 would crash)
    # TODO: k = k % len(items), then join two slices
    return items


if __name__ == "__main__":
    original = [1, 2, 3, 4, 5]
    print(rotate(original, 2))   # [4, 5, 1, 2, 3]
    print(original)              # still [1, 2, 3, 4, 5]
