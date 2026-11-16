# Arrays, two pointers and sliding windows

## Why this matters

Lists are the data structure you'll use most, and list problems are the most common kind in junior interviews. Many of them have an obvious O(n²) answer (try every pair, try every stretch) and a clever O(n) answer that uses one of three patterns: **two pointers**, the **sliding window** and **prefix sums**. Learn to recognise these three and a large share of "array" questions become routine.

## 1. How a Python list is laid out

An **array** is a block of memory holding items side by side, numbered from 0. A Python `list` is a **dynamic array**: an array that grows when it fills up.

```
index:     0      1      2      3      4     (spare) (spare) (spare)
        +------+------+------+------+------+-------+-------+-------+
        |  ref |  ref |  ref |  ref |  ref |       |       |       |
        +------+------+------+------+------+-------+-------+-------+
           |      |      |      |      |
           3      1      4      1      5      (the actual objects live elsewhere)
```

Each slot holds a **reference** (the memory address of an object), and every reference is the same size. That's why `nums[3]` is O(1): Python computes "start of block + 3 × slot size" and jumps straight there, no matter how long the list is.

The layout explains the costs you met in the lesson "Big-O from zero":

- **The end is cheap.** `append` writes into a spare slot; `pop()` clears the last one. O(1).
- **The front is expensive.** `insert(0, x)` has to move every existing reference one slot to the right to make room; `pop(0)` moves them all left. O(n).
- **Growing is occasional.** When the spare slots run out, Python allocates a bigger block (about 1.125× plus a bit) and copies everything. Rare enough that `append` is O(1) amortised.

```python
nums = [3, 1, 4]
nums.append(1)     # [3, 1, 4, 1]      O(1)
nums.insert(0, 9)  # [9, 3, 1, 4, 1]   O(n): four items shifted right
nums.pop(0)        # [3, 1, 4, 1]      O(n): four items shifted left
print(nums[2])     # 4                 O(1)
```

> **Note:** Strings are arrays of characters too, with one difference: they're **immutable** (they can't be changed). `s[i]` is O(1), but `s = s + "x"` builds a whole new string, which is O(len(s)). Building a string in a loop that way is O(n²); collect the pieces in a list and `"".join(parts)` once at the end instead.

## 2. Two pointers

**The problem.** Given a list sorted from smallest to largest, find two numbers that add up to a target.

The brute-force answer tries every pair: O(n²).

```python
def pair_brute_force(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None
```

The brute force ignores the one useful fact we were given: the list is **sorted**. Put one pointer (just an index variable) at each end:

```
target = 10
nums:   1    3    4    6    9
        ^                   ^
       left               right       1 + 9 = 10  ✓ found
```

Try another target, 7:

```
step 1:  1  3  4  6  9    1 + 9 = 10  too big   -> move right left (to a smaller number)
         L           R
step 2:  1  3  4  6  9    1 + 6 = 7   found
         L        R
```

Why is it safe to move `right` when the sum is too big? Because `nums[right]` plus the **smallest** remaining number is already too big, so `nums[right]` can't be part of any answer. Throw it away. By the same logic, when the sum is too small, `nums[left]` plus the **biggest** remaining number is too small, so `nums[left]` can go. Each step discards one item for good, so there are at most `n` steps: **O(n) time, O(1) space**.

```python
def pair_with_sum(sorted_nums, target):
    left, right = 0, len(sorted_nums) - 1
    while left < right:
        total = sorted_nums[left] + sorted_nums[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1
        else:
            right -= 1
    return None

print(pair_with_sum([1, 3, 4, 6, 9], 7))    # (0, 3)
print(pair_with_sum([1, 3, 4, 6, 9], 100))  # None
```

**When to reach for two pointers:** the input is sorted (or you can sort it), and you're looking for a pair, or comparing things from both ends. Other classic uses: checking whether a string is a palindrome (one pointer at each end, moving inward), reversing a list in place, and removing duplicates from a sorted list (a "slow" pointer that writes and a "fast" one that reads).

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("racecar"))  # True
print(is_palindrome("rocket"))   # False
```

## 3. The sliding window

**The problem.** Find the largest sum of any 3 neighbouring numbers in `[2, 1, 5, 1, 3, 2]`.

A **subarray** (or, for strings, a **substring**) is a stretch of neighbouring items. Brute force sums every stretch of 3 from scratch. That's O(n × k) for window size `k`, which is O(n²) when `k` grows with `n`.

Notice that neighbouring windows share almost everything:

```
[2, 1, 5] 1, 3, 2        sum = 8
 2,[1, 5, 1] 3, 2        sum = 8 - 2 + 1 = 7
 2, 1,[5, 1, 3] 2        sum = 7 - 1 + 3 = 9   <- best
 2, 1, 5,[1, 3, 2]       sum = 9 - 5 + 2 = 6
```

When the window slides one step right, one number enters and one leaves. Update the sum with one addition and one subtraction instead of re-adding all `k` numbers:

```python
def max_window_sum(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]   # add the newcomer, drop the leaver
        best = max(best, window)
    return best

print(max_window_sum([2, 1, 5, 1, 3, 2], 3))  # 9
```

That's O(n) time and O(1) space.

**Windows that grow and shrink.** Some problems don't fix the window size. "Find the longest substring with no repeated character" uses a window with a `left` and a `right` edge. Move `right` forward one character at a time; whenever the window becomes invalid (a repeat appears), move `left` forward until it's valid again.

```
s = "abcabcbb"
right=0  "a"          len 1
right=1  "ab"         len 2
right=2  "abc"        len 3   <- best
right=3  "abca"  repeat 'a': move left past the old 'a' -> "bca"   len 3
right=4  "bcab"  repeat 'b': -> "cab"                                len 3
...
```

```python
def longest_unique_substring(s):
    last_seen = {}   # character -> latest index
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1     # jump past the earlier copy
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best

print(longest_unique_substring("abcabcbb"))  # 3
print(longest_unique_substring("pwwkew"))    # 3
```

Both edges only ever move forward, so each character is handled a constant number of times: O(n).

**When to reach for a sliding window:** the question is about a **contiguous** stretch (subarray or substring): "longest", "shortest", "maximum sum of size k", "contains all of these letters".

## 4. Prefix sums

**The problem.** You have a list of daily sales and many questions of the form "total from day 10 to day 40?". Each question summed directly is O(n); a thousand questions is O(n × q).

Build a running total once. `prefix[i]` is the sum of the first `i` numbers, so `prefix[0]` is 0:

```
nums   =    [3,  1,  4,  1,  5]
prefix = [0, 3,  4,  8,  9, 14]
```

The sum from index `left` to `right` (both included) is "everything up to `right`" minus "everything before `left`":

```
sum(nums[left..right]) = prefix[right + 1] - prefix[left]

sum(nums[1..3]) = 1 + 4 + 1 = 6
                = prefix[4] - prefix[1] = 9 - 3 = 6   ✓
```

```python
from itertools import accumulate

nums = [3, 1, 4, 1, 5]
prefix = [0] + list(accumulate(nums))
print(prefix)                  # [0, 3, 4, 8, 9, 14]
print(prefix[3 + 1] - prefix[1])  # 6
```

Building the list is O(n) once; each question is then O(1). Total O(n + q). `itertools.accumulate` computes the running totals for you, but writing the loop yourself (as in the "Range sums with prefix sums" exercise) is a good way to understand it.

**When to reach for prefix sums:** many "sum of a range" questions on data that doesn't change.

## 5. Choosing a pattern

```
The question says...                                   Try...
"sorted", "pair", "two numbers that", "palindrome"     two pointers
"contiguous", "subarray/substring", "window of k",     sliding window
  "longest/shortest stretch"
"sum between i and j", many queries                    prefix sums
"unsorted", "pair that sums to"                        a hash map (next lesson)
```

Patterns are a starting point, not a rule. If you can't see one, write the brute force first, say its Big-O out loud, then ask: "what work am I repeating?" The repeated work is where the pattern hides.

## Common mistakes

**`IndexError: list index out of range`.** The classic off-by-one. The last valid index is `len(nums) - 1`, so `right = len(nums)` as a starting point reads past the end. Read the traceback's last line, then check the line number it points to: which index did you compute there?

**`while left <= right` in pair-finding.** With `<=`, the pointers can meet and you'd add a number to itself. For pairs, use `<`.

**Using two pointers on unsorted data.** The "discard one end" argument only works if the list is sorted. On unsorted input you'll silently get wrong answers, not an error. Sort first (O(n log n)) or use a hash map.

**Re-summing the window.** `sum(nums[i:i + k])` inside the loop looks like one line but is an O(k) slice plus an O(k) sum every iteration. That's the brute force in disguise.

**Forgetting the edge cases.** Empty list, a window bigger than the list, all-negative numbers (don't start `best` at 0). Test them before you call it done.

## Recap

- A Python list is a dynamic array: indexing and the end are O(1); the front is O(n).
- **Two pointers** on sorted input discard one item per step: O(n) instead of O(n²).
- A **sliding window** reuses the previous window's work as it moves: O(n) for contiguous-stretch problems.
- **Prefix sums** turn each range-sum question into one subtraction after O(n) set-up.
- Start from brute force, name its cost, then look for the repeated work.
