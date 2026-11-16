# Recursion and binary search

## Why this matters

Some problems are made of smaller copies of themselves: a folder contains folders, a comment thread contains replies with replies, a tree has subtrees. **Recursion** (a function that calls itself) is the natural way to write code for them, and you'll need it for the trees and graphs in the lesson "Trees, graphs and heaps". **Binary search** is the other half of this lesson: the O(log n) way to find things in sorted data, and one of the most frequently asked (and most frequently bungled) interview algorithms.

## 1. The call stack

Before recursion makes sense, you need to know what Python does when one function calls another.

```python
def greet(name):
    message = shout(name)
    return message + "!"

def shout(text):
    return text.upper()

print(greet("ada"))  # ADA!
```

When `greet` calls `shout`, `greet` is paused mid-line. Python needs to remember where it was and what its local variables were, so it keeps a **call stack**: a pile of **frames**, one per function call that hasn't finished yet. Each frame holds that call's local variables and its place in the code.

```
calling shout:             shout returns:            greet returns:
+-----------------+
| shout           |
| text = "ada"    |
+-----------------+        +-----------------+
| greet           |        | greet           |
| name = "ada"    |        | name = "ada"    |
| (waiting)       |        | message = "ADA" |
+-----------------+        +-----------------+       (stack empty)
```

A new call pushes a frame on top; a `return` pops it off, and the frame underneath carries on. Last in, first out, which is why it's called a stack (the lesson "Stacks, queues and linked lists" builds one).

> **Try it:** paste the code above into Python Tutor (linked below) and step through it. Watching the frames appear and disappear is the fastest way to understand everything that follows.

## 2. A function that calls itself

Here's a countdown written with recursion:

```python
def countdown(n):
    if n == 0:              # base case: stop
        print("liftoff")
        return
    print(n)
    countdown(n - 1)        # recursive case: a smaller problem

countdown(3)
# 3
# 2
# 1
# liftoff
```

Every recursive function has two parts:

1. **The base case:** an input small enough to answer directly, without recursing. Here, `n == 0`.
2. **The recursive case:** do a little work, then call yourself on a **smaller** input, one that's closer to the base case. Here, `n - 1`.

Each call gets its own frame with its own `n`. Calling `countdown(3)` stacks up four frames (`n = 3, 2, 1, 0`) before the base case returns and they unwind.

A recursive function that **returns a value** combines the answer from the smaller problem with its own work. The sum of a list is "the first item plus the sum of the rest":

```python
def total(nums):
    if not nums:                     # base case: empty list
        return 0
    return nums[0] + total(nums[1:])

print(total([4, 2, 7]))  # 13
```

Trace it to see the stack build up and then unwind:

```
total([4, 2, 7])
= 4 + total([2, 7])
      = 2 + total([7])
            = 7 + total([])
                  = 0             <- base case
            = 7 + 0 = 7
      = 2 + 7 = 9
= 4 + 9 = 13
```

**How to write one, in five steps** (the Reducible video below covers this well):

1. What's the simplest possible input? Write its answer: that's your base case.
2. Pick a slightly bigger input and imagine the function **already works** on anything smaller.
3. How would you build the answer for the bigger input from the smaller answer?
4. Generalise that into the recursive case.
5. Check that every call moves toward the base case.

Step 2 is the leap of faith. Don't try to trace every level in your head; trust that the smaller call works, as long as the base case is right and you always move toward it.

## 3. Where recursion shines: nested structures

`total` is easy as a loop too. Recursion earns its place when the data itself is nested to an unknown depth:

```python
def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))   # a list inside: same problem, smaller
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], [], 5]))  # [1, 2, 3, 4, 5]
```

Writing that with plain loops is awkward, because you don't know how many levels deep to go.

Recursion is also good at **halving** a problem. Computing `base ** exp` by multiplying `exp` times is O(exp). But `2¹⁰ = (2⁵)²`, so one recursive call on half the exponent does the job:

```python
def power(base, exp):
    if exp == 0:
        return 1
    half = power(base, exp // 2)
    if exp % 2 == 0:
        return half * half
    return half * half * base

print(power(2, 10))  # 1024
```

Each call halves `exp`, so there are about `log₂ exp` calls: O(log n), the same shape as binary search.

## 4. Recursion vs loops, and RecursionError

Anything recursive can be written with a loop (sometimes with your own stack), and anything with a loop can be written recursively. Choose whichever is clearer. In Python, prefer loops for simple repetition, for two reasons:

- **Every call costs a frame.** That's O(depth) memory, plus overhead. `total` above also copies the list with `nums[1:]` on every call, making it O(n²) in disguise.
- **Python limits the depth.** By default the stack may hold about 1,000 frames. Go deeper and you get:

```python
total(list(range(5000)))
# RecursionError: maximum recursion depth exceeded
```

You'll see the same error, after a long traceback of identical lines, if you **forget the base case** or your recursive case doesn't move toward it. The repeated lines are the giveaway: read the last few to see which function is calling itself, then check its base case.

> **Note:** You can raise the limit with `sys.setrecursionlimit`, but that's almost never the right fix. If the depth can grow with the input size, use a loop.

**Overlapping calls can explode.** Counting the right/down paths across a grid looks innocent:

```python
def count_paths(rows, cols):
    if rows == 1 or cols == 1:
        return 1
    return count_paths(rows - 1, cols) + count_paths(rows, cols - 1)

print(count_paths(3, 3))  # 6
```

But each call makes two more, and the same smaller grids get recomputed over and over. The running time grows exponentially, so `count_paths(18, 18)` already takes ages. Remembering answers you've already computed (with `functools.cache`) fixes it; that idea is the doorway to **dynamic programming**, linked at the end of the lesson "Trees, graphs and heaps".

## 5. Binary search

You're looking for a name in a 1,000-page printed phone book. You don't start at page 1. You open the middle, see whether your name comes before or after, and throw away the half it can't be in. Repeat. Ten halvings get you from 1,000 pages to one.

That's **binary search**, and it needs one thing: the data must be **sorted**.

```
find 23 in:   2   5   8  12  16  23  38  56  72  91
index:        0   1   2   3   4   5   6   7   8   9

lo=0 hi=9  mid=4  nums[4]=16 < 23   -> answer is right of mid: lo=5
lo=5 hi=9  mid=7  nums[7]=56 > 23   -> answer is left of mid:  hi=6
lo=5 hi=6  mid=5  nums[5]=23 == 23  -> found at index 5
```

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(nums, 23))  # 5
print(binary_search(nums, 4))   # -1
```

Each loop halves the range, so it's **O(log n)**: about 20 steps for a million items, 30 for a billion. Compare that with `x in my_list`, which is O(n).

**The loop invariant.** Binary search is famous for off-by-one bugs. The way to get it right is to decide exactly what `lo` and `hi` mean and keep that true on every pass (that promise is called a **loop invariant**). Here: "if `target` is in the list, it's somewhere in `nums[lo..hi]`, both ends included". Then:

- The loop runs `while lo <= hi`, because a range with `lo == hi` still contains one item to check.
- After checking `mid`, we know it's not the answer, so exclude it: `lo = mid + 1` or `hi = mid - 1`. Writing `lo = mid` here can loop forever.
- When `lo > hi` the range is empty, so the target isn't there.

## 6. Lower bound and the `bisect` module

Often you don't want "is it there?" but "**where would it go?**": the first position whose value is `>= target`. That's called the **lower bound**, and it also handles duplicates (it finds the *first* copy).

```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)            # note: hi is len(nums), not len - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1             # answer is after mid
        else:
            hi = mid                 # mid might be the answer: keep it
    return lo

print(lower_bound([1, 3, 3, 3, 8], 3))  # 1
print(lower_bound([1, 3, 3, 3, 8], 9))  # 5   (past the end)
```

The invariant is different this time ("the answer is in the half-open range `[lo, hi)`"), so the loop condition and updates differ too. That's the point: pick the invariant first, then the code follows.

In real code, use the standard library's `bisect` module, which does exactly this:

```python
import bisect

scores = [10, 20, 20, 30]
print(bisect.bisect_left(scores, 20))   # 1   first position for 20
print(bisect.bisect_right(scores, 20))  # 3   position after the last 20
bisect.insort(scores, 25)               # insert, keeping it sorted
print(scores)                           # [10, 20, 20, 25, 30]
```

> **Note:** `insort` finds the spot in O(log n) but inserting into a list is still O(n), because items shift over.

**Binary search on the answer.** The same idea works on questions that aren't about lists at all. "What's the smallest page-per-day speed that finishes this book list in 10 days?" If you can check a guess quickly, and every speed above a working one also works, you can binary-search the speed instead of trying each one. You won't need this often as a junior, but when an interviewer says "minimum value such that…", think of it.

## Common mistakes

**`RecursionError: maximum recursion depth exceeded`.** Either the base case is missing or unreachable, or the input is genuinely too deep for recursion. Check that each call gets smaller; if it's depth, switch to a loop.

**Forgetting to `return` the recursive result.** `power(base, exp // 2)` on its own line computes the answer and throws it away; the function then returns `None`. You'll see `TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'` one level up.

**Binary search on unsorted data.** No error, just wrong answers. Sort first or don't use it.

**`lo = mid` in a `while lo <= hi` loop.** When `lo == hi`, `mid` equals `lo` and nothing changes: an infinite loop. Pair each loop condition with the right updates, as shown above.

**Mixing up `len(nums)` and `len(nums) - 1` for `hi`.** It depends on the invariant: inclusive range uses `len - 1`, half-open uses `len`. Pick one and stay consistent.

## Recap

- The **call stack** holds one frame per unfinished call; recursion just stacks frames of the same function.
- A recursive function needs a **base case** and a **recursive case** that moves toward it.
- Recursion suits nested data and halving problems; use loops for simple repetition, because Python limits depth to about 1,000.
- **Binary search** halves a sorted range each step: O(log n). Decide what `lo` and `hi` mean (the invariant) and the code follows.
- Use `bisect` in real code; know how to write it for interviews.
