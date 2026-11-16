def chunked(iterable, size: int):
    """Yield lists of `size` items from iterable; the last one may be shorter."""
    # TODO: raise ValueError if size < 1
    # TODO: collect items into a list; when it has `size` items, yield it and start a new one
    # TODO: after the loop, yield the leftover items if there are any
    yield from ()


if __name__ == "__main__":
    import itertools

    print(list(chunked([1, 2, 3, 4, 5], 2)))  # want [[1, 2], [3, 4], [5]]
    print(list(itertools.islice(chunked(itertools.count(), 3), 2)))  # want [[0, 1, 2], [3, 4, 5]]
