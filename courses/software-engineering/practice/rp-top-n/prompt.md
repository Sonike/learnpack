# The most common words, with Counter

Counting things is so common that the standard library has a tool for it: `collections.Counter`. Use it instead of writing the counting loop yourself.

```python
def top_n(words: list[str], n: int) -> list[tuple[str, int]]:
```

- `words` is a list of words, e.g. from `text.split()`.
- Count them **case-insensitively** (`"The"` and `"the"` are the same word; report it in lowercase). Ignore empty strings.
- Return the `n` most common as `(word, count)` tuples, most common first. Words with equal counts keep the order in which they first appeared (that's what `Counter.most_common` does).
- If `n` is larger than the number of different words, return them all. If `n` is 0 or less, return `[]`.

## Example

```python
top_n(["the", "cat", "The", "dog", "the", "cat"], 2)   # [("the", 3), ("cat", 2)]
top_n(["a", "b"], 10)                                  # [("a", 1), ("b", 1)]
```
