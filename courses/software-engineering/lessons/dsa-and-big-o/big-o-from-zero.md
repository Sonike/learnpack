# Big-O from zero

## Why this matters

A function that feels instant on 10 items can freeze a server on 10 million. Engineers need a quick way to say "this code will be fine" or "this will fall over when we grow" before running it on real data, and **Big-O notation** is that shared language. It is also the first thing a junior interviewer checks after "does it work?": almost every coding interview ends with "what's the time and space complexity?"

## 1. Work grows with the input

Here are two ways to check whether a list contains a value twice:

```python
def has_duplicate_slow(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def has_duplicate_fast(items):
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False
```

Both give the same answers. On a list of 5 items you'd never notice a difference. Now count how much work each one does when there is **no** duplicate (the worst case, because neither can stop early):

```
n (items)    slow: pairs compared    fast: items looked at
       10                       45                       10
      100                    4,950                      100
    1,000                  499,500                    1,000
1,000,000          499,999,500,000                1,000,000
```

At a million items the slow version does half a trillion comparisons: hours of work. The fast one does a million: a fraction of a second. The difference isn't the computer or the language. It's **how the work grows** as `n`, the size of the input, grows.

That's all Big-O describes. Not seconds (those depend on your laptop), but the *shape* of the growth.

> **Try it:** the practice exercise "Count the steps: quadratic vs linear" has you add step counters to both versions and watch the numbers above appear.

## 2. Counting steps

To find the shape, count the basic steps (a comparison, an addition, reading a list item) as a formula in `n`.

```python
def total(nums):
    result = 0           # 1 step
    for x in nums:       # the loop body runs n times
        result += x      # 1 step each time
    return result        # 1 step
```

That's `n + 2` steps. For the slow duplicate check, the inner comparison runs once for every pair, which is `n × (n − 1) / 2 = 0.5n² − 0.5n` steps.

Now two simplifications, which are the whole trick of Big-O:

1. **Drop the constants.** `3n` and `n` grow the same way: double the input and both double. Whether one step costs 1 or 3 nanoseconds depends on hardware, so we ignore the multiplier.
2. **Keep only the biggest term.** In `0.5n² − 0.5n`, once `n` is large the `n²` part is so much bigger that the rest doesn't matter. At `n = 1,000,000`, `n²` is a trillion and `n` is a million.

So `n + 2` becomes **O(n)** (read "big O of n" or "order n"), and `0.5n² − 0.5n` becomes **O(n²)**. The `O` means "grows no faster than, ignoring constants".

```
3n + 5          →  O(n)
0.5n² + 100n    →  O(n²)
7               →  O(1)
2n + log n      →  O(n)
```

## 3. The six growth rates you'll meet

Nearly every algorithm you'll be asked about is one of these. Here they are from fastest to slowest, each with a real Python example.

**O(1), constant.** The work doesn't depend on `n` at all.

```python
def first(items):
    return items[0]        # same cost for a list of 3 or 3 million

prices = {"apple": 3, "pear": 5}
print(prices["pear"])      # 5   dict lookup: O(1) on average
```

**O(log n), logarithmic.** Each step throws away half of what's left. `log₂ n` is "how many times can I halve `n` before reaching 1?" For a million that's only about 20.

```python
def halvings(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps

print(halvings(8))          # 3
print(halvings(1_000_000))  # 19
```

Binary search (looking up a word in a sorted dictionary by opening it in the middle) is the classic O(log n) algorithm.

**O(n), linear.** You touch each item a constant number of times.

```python
def largest(nums):
    best = nums[0]
    for x in nums:
        if x > best:
            best = x
    return best

print(largest([4, 9, 2]))  # 9
```

**O(n log n), linearithmic.** Typical of good sorting algorithms: split the problem in halves (`log n` levels), doing O(n) work at each level. Python's `sorted()` is O(n log n).

**O(n²), quadratic.** A loop over the items inside another loop over the items, like the slow duplicate check. Fine for 1,000 items, painful for 100,000.

**O(2ⁿ), exponential.** The work *doubles* every time `n` grows by one. It usually comes from trying every combination:

```python
def all_subsets(items):
    if not items:
        return [[]]
    rest = all_subsets(items[1:])
    return rest + [[items[0]] + s for s in rest]

print(len(all_subsets([1, 2, 3])))      # 8
print(len(all_subsets(list(range(20)))))  # 1048576
```

At 40 items that's a trillion subsets. Exponential algorithms are only usable on tiny inputs.

Here is how they compare at a few sizes:

```
n          O(1)  O(log n)   O(n)     O(n log n)   O(n²)          O(2ⁿ)
10         1     3          10       33           100            1,024
1,000      1     10         1,000    ~10,000      1,000,000      (astronomical)
1,000,000  1     20         10⁶      ~2×10⁷       10¹²           (astronomical)
```

A useful rule of thumb: a typical computer does roughly 10⁷ to 10⁸ simple Python steps per second. So 10¹² steps is hours, and 2×10⁷ is a second or so.

> **Try it:** the exercise "Guess the Big-O from measurements" turns this table around: given measured step counts, you work out which growth rate produced them.

## 4. Reading Big-O from code

You rarely count every step. Instead, look at the structure.

**Sequential loops add.** Two loops one after the other are `n + n = 2n`, which is still **O(n)**:

```python
def min_and_max(nums):
    low = min(nums)    # one pass: O(n)
    high = max(nums)   # another pass: O(n)
    return low, high   # total O(n), not O(n²)
```

**Nested loops multiply.** A loop of `n` inside a loop of `n` is `n × n`, **O(n²)**. If the inner loop runs over a *different* input of size `m`, it's **O(n × m)**; don't call two different sizes both `n`.

**A loop that halves is logarithmic.** `while n > 1: n //= 2` runs about `log₂ n` times, so it's O(log n). A loop that goes `i = 1, 2, 4, 8, …` up to `n` is the same.

**Hidden loops count.** A single line can hide a loop. `x in my_list` walks the list, so this innocent-looking function is O(n²):

```python
def common(a, b):
    result = []
    for x in a:          # n times
        if x in b:       # each check walks b: O(n)
            result.append(x)
    return result
```

Turning `b` into a set first (`b_set = set(b)`, O(n) once) makes each check O(1) on average, and the whole function O(n).

## 5. Best, worst and average case

The same function can do very different amounts of work depending on *which* input it gets, not just how big it is.

```python
def find(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```

- **Best case:** the target is first. One step, O(1).
- **Worst case:** the target is last or missing. `n` steps, O(n).
- **Average case:** on random positions, about `n/2` steps, still O(n).

When people say "this is O(n)" without qualification, they almost always mean the **worst case**, because that's the one that pages you at 3 a.m. Some algorithms are quoted by their average case when the worst case is very rare; dict lookup is O(1) on average but O(n) in a pathological worst case, and you'll see why in the lesson on hash maps.

> **Note:** You may see Ω (omega) and Θ (theta) in textbooks and in the CS50 lecture. Roughly, O is an upper bound ("no worse than"), Ω a lower bound ("no better than") and Θ means both. In interviews and day-to-day work, people say O and mean "tight upper bound".

## 6. Space complexity

Time isn't the only cost. **Space complexity** is how much *extra* memory an algorithm needs as `n` grows (not counting the input itself).

```python
def total(nums):          # O(1) extra space: one number, whatever n is
    result = 0
    for x in nums:
        result += x
    return result

def doubled(nums):        # O(n) extra space: builds a new list of n items
    return [x * 2 for x in nums]
```

`has_duplicate_fast` above uses O(n) space for its `seen` set, while the slow version uses O(1). That's a common trade: **spend memory to save time**. Usually it's a good deal, but you should be able to say you're making it.

## 7. What Python operations cost

You can't reason about Python code without knowing what the built-ins do underneath. These are worth memorising (n is the size of the collection):

```
Operation                       Cost         Why
list[i], list[i] = x            O(1)         jump straight to position i
list.append(x)                  O(1)*        add at the end (* amortised, see below)
list.pop()                      O(1)         remove from the end
list.insert(0, x), list.pop(0)  O(n)         every other item shifts over
x in list, list.index(x)        O(n)         walks the list
list[a:b]                       O(b − a)     slicing copies the items
len(list)                       O(1)         the length is stored
x in set, x in dict             O(1) avg     hashing (lesson on hash maps)
dict[key], dict[key] = v        O(1) avg
sorted(list), list.sort()       O(n log n)
min(list), max(list), sum(list) O(n)
```

**Amortised** means "on average over many calls". A Python list keeps some spare room at the end. Most appends just use the spare room (O(1)); once in a while the list is full and Python copies everything into a bigger block (O(n)). Because the new block is proportionally bigger each time, those copies are rare enough that the average cost per append stays O(1).

> **Note:** The Python Wiki's "Time Complexity" page, linked below, lists these for every built-in type. Keep it open while you practise.

## Common mistakes

**Calling two sequential loops O(n²).** Loops one after another add; only loops inside each other multiply. `for` then `for` is O(n).

**Forgetting hidden loops.** `in` on a list, `.index()`, `.count()`, `.remove()`, slicing, `list.insert(0, …)` and string concatenation in a loop are all O(n) per call. A loop that calls one of them is O(n²).

**Keeping constants.** "O(2n)" or "O(n/2)" isn't wrong exactly, but it signals you haven't simplified. Say O(n).

**Mixing up sizes.** A function that loops over `users` and, inside, over `orders` is O(u × o), not O(n²). If the interviewer says "assume orders is small", it becomes effectively O(u).

**Assuming fast hardware saves you.** A computer 10× faster lets an O(n²) algorithm handle only about 3× more data in the same time (√10 ≈ 3.2). A better algorithm wins every time.

**What you'll see when it goes wrong.** There's no error message for "too slow". The program just hangs, and in an online judge you get **Time Limit Exceeded**. When that happens, look for nested loops and hidden O(n) calls before you look anywhere else.

**About AI tools:** an assistant will happily tell you the Big-O of a snippet, and it's often right. Work it out yourself first, then compare. Interviewers ask you to explain *why*, and that only comes from doing it.

## Recap

- Big-O describes how work grows with input size `n`, ignoring constants and smaller terms.
- From fast to slow: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ).
- Sequential loops add (still O(n)); nested loops multiply (O(n²)); halving loops are O(log n).
- Quote the worst case unless you say otherwise; average case matters for hash-based structures.
- Space complexity counts the extra memory you use; trading space for time is common.
- Know the costs of Python built-ins: `append` and dict/set lookups are O(1); `in` on a list, `insert(0, …)` and slicing are O(n).
