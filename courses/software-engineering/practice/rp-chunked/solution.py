def chunked(iterable, size: int):
    """Yield lists of `size` items from iterable; the last one may be shorter."""
    if size < 1:
        raise ValueError(f"size must be at least 1, got {size}")
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
