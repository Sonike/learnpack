# A lazy chunking generator

Sending 1,000,000 rows to a database one at a time is slow; sending them in batches of 500 is fast. Write a **generator** that splits any iterable into chunks, without ever building the whole result in memory.

```python
def chunked(iterable, size: int):
```

- `iterable` is anything you can loop over: a list, a file, a `range`, even an endless iterator like `itertools.count()`.
- `size` is how many items go in each chunk.
- **Yield** lists of `size` items, in order. The last chunk may be shorter. Nothing is yielded for an empty iterable.
- If `size` is less than 1, raise `ValueError`. (Because this is a generator, the error appears when someone first asks for a chunk, not when `chunked(...)` is called. That's fine.)
- Be lazy: only pull as many items from `iterable` as you need for the chunk being yielded. The tests feed you an endless iterator, so building a full list first would never finish.

## Example

```python
list(chunked([1, 2, 3, 4, 5], 2))    # [[1, 2], [3, 4], [5]]

import itertools
list(itertools.islice(chunked(itertools.count(), 3), 2))   # [[0, 1, 2], [3, 4, 5]]
```
