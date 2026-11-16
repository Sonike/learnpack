# Count the words

Counting things is one of the most common jobs a dict does: **key** = the thing, **value** = how many times you've seen it.

```python
def word_counts(text: str) -> dict[str, int]: ...
```

- `text` is any text: sentences, punctuation, mixed case.
- Split it into words on whitespace (`text.split()`).
- Make each word lowercase and strip punctuation **from its ends** with `word.strip(string.punctuation)` (so `"Hello,"` → `"hello"`, but `"don't"` stays `"don't"`).
- Skip anything that's empty after stripping (like a lone `"—"` or `"!"`).
- Return a dict mapping each word to how many times it appears.

## Example

```python
word_counts("The cat saw the other cat. THE END!")
# {"the": 3, "cat": 2, "saw": 1, "other": 1, "end": 1}
word_counts("")
# {}
```
