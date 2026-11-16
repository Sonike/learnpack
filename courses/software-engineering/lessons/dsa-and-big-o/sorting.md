# Sorting

## Why this matters

In real work you'll sort with one line, `sorted(items)`, and you should. But sorting is how interviewers check that you understand Big-O, recursion and trade-offs, and "sort it first" is the hidden first step in a surprising number of problems: once data is in order, duplicates sit next to each other, overlaps become easy to spot and binary search becomes possible. This lesson builds two sorts by hand so `sorted()` stops being magic, then shows how to use it well.

## 1. Selection sort: the obvious way

Ask someone to sort a hand of cards and they'll often do this: find the smallest card, put it first; find the smallest of the rest, put it second; and so on.

```
[5, 2, 9, 1]    smallest is 1 -> swap into position 0
[1, 2, 9, 5]    smallest of the rest is 2, already in place
[1, 2, 9, 5]    smallest of the rest is 5 -> swap into position 2
[1, 2, 5, 9]    done
```

```python
def selection_sort(items):
    result = list(items)                    # don't change the caller's list
    for i in range(len(result)):
        smallest = i
        for j in range(i + 1, len(result)):
            if result[j] < result[smallest]:
                smallest = j
        result[i], result[smallest] = result[smallest], result[i]
    return result

print(selection_sort([5, 2, 9, 1]))  # [1, 2, 5, 9]
```

Finding each minimum scans the rest of the list: `n − 1`, then `n − 2`, … comparisons, about `n²/2` in total. That's **O(n²)**, and it's O(n²) every time, even on a list that's already sorted, because it never stops looking early.

## 2. Insertion sort: good on nearly-sorted data

Another way to sort cards: pick them up one at a time and slide each new card left into its place among the cards you're already holding.

```
[5 | 2, 9, 1]      the part left of | is sorted
[2, 5 | 9, 1]      2 slides left past 5
[2, 5, 9 | 1]      9 is already bigger than 5: stays
[1, 2, 5, 9 |]     1 slides left past 9, 5, 2
```

```python
def insertion_sort(items):
    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and result[j] > current:   # shift bigger items right
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current                 # drop into the gap
    return result

print(insertion_sort([5, 2, 9, 1]))  # [1, 2, 5, 9]
```

- **Worst case**, a list in reverse order: every item slides all the way left. About `n²/2` shifts, **O(n²)**.
- **Best case**, an already-sorted list: the `while` test fails immediately for every item. One comparison each, **O(n)**.

That best case is what makes insertion sort genuinely useful. On small or nearly-sorted lists it's very fast, so real-world sorting algorithms (including Python's) use it for short runs.

## 3. Merge sort: divide and conquer

To beat O(n²), stop comparing everything with everything. **Divide and conquer** means: split the problem into smaller copies, solve those (recursively), then combine the answers.

For sorting:

1. **Divide:** split the list in half.
2. **Conquer:** merge-sort each half (a list of 0 or 1 items is already sorted: that's the base case).
3. **Combine:** **merge** the two sorted halves into one sorted list.

Merging is the clever part, and it's cheap. Both halves are sorted, so the smallest remaining item is always at the front of one of them. Keep taking the smaller front:

```
left:  [2, 5]      right: [1, 9]      merged: []
          ^                  ^         1 < 2   take 1
left:  [2, 5]      right: [1, 9]      merged: [1]
          ^                     ^      2 < 9   take 2
left:  [2, 5]      right: [1, 9]      merged: [1, 2]
             ^                  ^      5 < 9   take 5
left is empty: add the rest of right  merged: [1, 2, 5, 9]
```

Each step places one item, so merging two halves with `n` items in total is O(n).

```python
def merge_sort(items):
    if len(items) <= 1:                     # base case
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:             # <= keeps equal items in order
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])                 # one of these is empty
    merged.extend(right[j:])
    return merged

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))  # [3, 9, 10, 27, 38, 43, 82]
```

**Why O(n log n)?** Picture the splitting as levels:

```
level 0:         [38 27 43 3 9 82 10]             n items merged at this level
level 1:     [38 27 43]       [3 9 82 10]          n items in total
level 2:   [38] [27 43]     [3 9]  [82 10]         n items in total
level 3:        [27] [43]  [3] [9] [82] [10]       n items in total
```

Halving `n` until you reach single items takes about `log₂ n` levels, and each level does O(n) merging work in total. So: **O(n log n)** time, in the best, worst and average case. It also uses **O(n) extra space** for the merged lists.

How big is the difference? At a million items, `n²` is 10¹² and `n log n` is about 2 × 10⁷. That's the gap between hours and a fraction of a second.

> **Try it:** the CS50 "Algorithms" lecture and VisuAlgo's sorting page (both below) animate these algorithms. Watching merge sort's levels build up makes the `log n` click.

## 4. Stability

A sort is **stable** if items that compare equal keep their original order. Why care? Suppose a list of students is already in alphabetical order and you sort it by grade:

```python
students = [("Ada", "B"), ("Bob", "A"), ("Cy", "B"), ("Dee", "A")]
print(sorted(students, key=lambda s: s[1]))
# [('Bob', 'A'), ('Dee', 'A'), ('Ada', 'B'), ('Cy', 'B')]
```

Within each grade, the names are still alphabetical, because `sorted` is stable. That lets you sort by several things in steps: sort by the minor key first, then by the major key.

- **Insertion sort** is stable, as long as it only shifts items that are *strictly* bigger (`>` not `>=`).
- **Merge sort** is stable, as long as ties take from the *left* half (`<=` not `<`).
- **Selection sort** is **not** stable: its long-distance swaps can jump an item over an equal one.

## 5. What you use in real code: `sorted()` and Timsort

Python's `sorted()` and `list.sort()` use **Timsort**: a merge sort that first finds runs that are already in order and uses insertion sort on short stretches. It's stable, O(n log n) in the worst case and close to O(n) on nearly-sorted data. It's also written in C, so it beats any sort you write in Python by a wide margin. **Always use it in real code.**

```python
nums = [5, 2, 9, 1]
print(sorted(nums))          # [1, 2, 5, 9]    returns a new list
print(nums)                  # [5, 2, 9, 1]    unchanged
nums.sort()                  # sorts in place, returns None
print(nums)                  # [1, 2, 5, 9]
print(sorted(nums, reverse=True))  # [9, 5, 2, 1]
```

**Sorting with a key.** Pass `key=`, a function that turns each item into the value to compare:

```python
words = ["banana", "Fig", "apple", "cherry"]
print(sorted(words))                    # ['Fig', 'apple', 'banana', 'cherry']   capitals first!
print(sorted(words, key=str.lower))     # ['apple', 'banana', 'cherry', 'Fig']
print(sorted(words, key=len))           # ['Fig', 'apple', 'banana', 'cherry']

people = [{"name": "Ada", "age": 36}, {"name": "Bob", "age": 25}]
print([p["name"] for p in sorted(people, key=lambda p: p["age"])])  # ['Bob', 'Ada']
```

To sort by two things, return a tuple; tuples compare item by item. To reverse just one part of a numeric key, negate it:

```python
scores = [("ada", 90), ("bob", 85), ("cy", 90)]
print(sorted(scores, key=lambda s: (-s[1], s[0])))
# [('ada', 90), ('cy', 90), ('bob', 85)]   highest score first, then by name
```

## 6. Sorting as a first step

Many problems get easy once the data is sorted. Paying O(n log n) up front is often the whole trick.

**Merge overlapping intervals.** Bookings `(1, 3)`, `(8, 10)`, `(2, 6)` overlap in confusing ways. Sort by start time and an interval can only overlap the one just before it:

```python
def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:           # overlaps the last one
            merged[-1][1] = max(merged[-1][1], end)     # stretch it
        else:
            merged.append([start, end])
    return [tuple(pair) for pair in merged]

print(merge_intervals([(8, 10), (1, 3), (2, 6), (15, 18)]))
# [(1, 6), (8, 10), (15, 18)]
```

O(n log n) for the sort plus O(n) for the walk: O(n log n) overall.

**Can one person attend every meeting?** Sort by start; if any meeting starts before the previous one ends, no.

```python
def can_attend_all(meetings):
    meetings = sorted(meetings)
    for (s1, e1), (s2, e2) in zip(meetings, meetings[1:]):
        if s2 < e1:
            return False
    return True

print(can_attend_all([(9, 10), (13, 14), (10, 12)]))  # True
print(can_attend_all([(9, 11), (10, 12)]))            # False
```

Other places sorting helps: finding duplicates (they become neighbours), two pointers (which need sorted input) and binary search.

## Common mistakes

**`x = items.sort()` then using `x`.** `list.sort()` sorts in place and returns `None`, so `x` is `None`. You'll see `TypeError: 'NoneType' object is not subscriptable` the next time you index it. Use `x = sorted(items)` for a new list.

**`TypeError: '<' not supported between instances of 'str' and 'int'`.** You're sorting a mix of types that can't be compared, often numbers read from a file as strings next to real numbers. Convert them first, or pass a `key`.

**Sorting strings that hold numbers.** `sorted(["10", "9", "100"])` gives `['10', '100', '9']`: strings compare character by character. Use `key=int`.

**Uppercase before lowercase.** In character order all capitals come before all lowercase letters. Use `key=str.lower` for human-friendly order.

**Writing your own sort in production.** It'll be slower and buggier than `sorted()`. Hand-written sorts belong in interviews and in understanding, like this lesson.

**About AI tools:** ask an assistant to *explain* why merge sort is O(n log n) or to draw the levels for a list you choose. Write the merge loop yourself; its index juggling is exactly what interviews test.

## Recap

- **Selection sort:** always O(n²), not stable. **Insertion sort:** O(n²) worst, O(n) on sorted input, stable.
- **Merge sort:** divide in half, sort each, merge in O(n); `log n` levels make it O(n log n), with O(n) extra space. Stable.
- **Stable** sorts keep equal items in their original order, which lets you sort by several keys in steps.
- In real code use `sorted()` / `.sort()` (Timsort), with `key=` and tuple keys for custom orders.
- "Sort first" turns many problems, like merging intervals, into a simple walk.
