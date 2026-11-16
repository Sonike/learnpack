# Interview problem: word ladder (medium)

> **Note:** 35-minute timer. The key insight is recognising the pattern: "shortest number of steps" on a set of states is **breadth-first search** (BFS).

You can change a word one letter at a time, and every word you pass through must be in `words`. Return the number of words in the **shortest** sequence from `begin` to `end`, counting both `begin` and `end`. Return `0` if there's no such sequence.

Write `word_ladder_length(begin: str, end: str, words: list[str]) -> int`.

- All words are lowercase and the same length.
- `begin` doesn't need to be in `words`; `end` does (if it isn't, the answer is `0`).
- `begin` and `end` are different.

## Examples

```python
word_ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
# 5   (hit -> hot -> dot -> dog -> cog)
word_ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"])
# 0   ("cog" isn't in the list)
word_ladder_length("hot", "dot", ["dot"])
# 2
```

> **Hint:** BFS with `collections.deque`, starting from `(begin, 1)`. For a word, generate every neighbour by trying each letter `a`–`z` in each position, and keep those still in the unvisited set. Remove a word from the set when you queue it, so you never visit it twice.
