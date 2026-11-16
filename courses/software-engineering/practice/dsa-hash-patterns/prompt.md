# Three hash map patterns

Most "use a hash map" interview problems are one of three patterns: **seen-before**, **group by key** and **count**. Write one of each, all in O(n) time.

## 1. Two sum (seen-before)

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None: ...
```

Return indexes `(i, j)` with `i < j` and `nums[i] + nums[j] == target`, or `None`. The list is **not** sorted. Keep a dict from value to index of the numbers you've passed; for each new number, check whether `target - number` is in it.

```python
two_sum([2, 7, 11, 15], 9)  # (0, 1)
two_sum([3, 3], 6)          # (0, 1)
two_sum([1, 2], 10)         # None
```

If several pairs work, return the one whose **second** index is smallest (that's what the dict approach finds naturally).

## 2. Group anagrams (group by key)

```python
def group_anagrams(words: list[str]) -> list[list[str]]: ...
```

Anagrams use the same letters, like `"eat"`, `"tea"` and `"ate"`. Group them. The key for a word is its letters sorted: `"".join(sorted(word))`. Groups appear in the order their first word appeared, and words inside a group keep their input order.

```python
group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
# [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

## 3. First unique character (count)

```python
def first_unique_char(s: str) -> int: ...
```

Return the index of the first character that appears exactly once in `s`, or `-1`. Count with `collections.Counter`, then scan again.

```python
first_unique_char("leetcode")      # 0
first_unique_char("loveleetcode")  # 2
first_unique_char("aabb")          # -1
```
