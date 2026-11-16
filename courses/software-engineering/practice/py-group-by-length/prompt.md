# Group words by length

**Grouping** is counting's sibling: instead of a number per key, you keep a list per key.

```python
def group_by_length(words: list[str]) -> dict[int, list[str]]: ...
```

- `words` is a list of strings.
- Return a dict whose keys are word lengths and whose values are lists of the words with that length.
- Inside each list, keep the words **in the order they appeared** in `words` (duplicates included).
- The keys should appear in the order each length was first seen (a normal dict remembers insertion order, so this happens naturally).

## Example

```python
group_by_length(["hi", "cat", "a", "dog", "ok"])
# {2: ["hi", "ok"], 3: ["cat", "dog"], 1: ["a"]}
group_by_length([])
# {}
```
