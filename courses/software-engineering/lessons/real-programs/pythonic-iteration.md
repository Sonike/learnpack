# Pythonic iteration

Loops are the heart of most programs, and Python has a set of tools that make them shorter and clearer: comprehensions, `enumerate`, `zip`, sorting with keys, and generators. Experienced Python developers use these everywhere, so you need them to read real codebases, and interviewers notice when you use them well. The goal isn't cleverness; it's code that says what it does in as few moving parts as possible.

## List comprehensions

Here's a loop you've written many times: build a new list from an old one.

```python
prices = [4.0, 12.5, 7.25, 30.0]

with_vat = []
for p in prices:
    with_vat.append(round(p * 1.2, 2))

print(with_vat)   # [4.8, 15.0, 8.7, 36.0]
```

A **list comprehension** says the same thing in one expression:

```python
with_vat = [round(p * 1.2, 2) for p in prices]
print(with_vat)   # [4.8, 15.0, 8.7, 36.0]
```

Read it as "a list of `round(p * 1.2, 2)` for each `p` in `prices`". The shape is always:

```
[ expression   for item in iterable ]
   what to make  where it comes from
```

Add an `if` at the end to keep only some items:

```python
cheap = [p for p in prices if p < 10]
print(cheap)   # [4.0, 7.25]
```

Which reads: "`p`, for each `p` in `prices`, if `p` is under 10". The `if` filters; it decides *whether* an item is included. If you want to choose *between two values* for every item, that's a conditional expression, and it goes at the front:

```python
labels = ["cheap" if p < 10 else "pricey" for p in prices]
print(labels)   # ['cheap', 'pricey', 'cheap', 'pricey']
```

> **Try it:** in the practice editor, write `[n * n for n in range(1, 6)]`, then add `if n % 2 == 1`. Predict each result before you run it.

### Dict and set comprehensions

Swap the brackets and you can build dicts and sets the same way:

```python
names = ["Ada", "Grace", "Alan", "ada"]

lengths = {name: len(name) for name in names}
print(lengths)   # {'Ada': 3, 'Grace': 5, 'Alan': 4, 'ada': 3}

initials = {name[0].upper() for name in names}
print(initials)  # {'A', 'G'}   (a set has no duplicates; its order may differ)
```

A dict comprehension has `key: value` before the `for`. A set comprehension uses `{}` without a colon.

### Nested loops in a comprehension

Two `for` clauses read in the same order as the nested loops they replace:

```python
grid = [[1, 2, 3], [4, 5], [6]]

flat = []
for row in grid:
    for n in row:
        flat.append(n)

flat = [n for row in grid for n in row]
print(flat)   # [1, 2, 3, 4, 5, 6]
```

That's about the limit of what stays readable.

### When not to use a comprehension

Comprehensions are for **building a collection**. Use a normal loop when:

- You're doing something for its side effect, like printing or saving. `[print(x) for x in items]` builds a useless list of `None`s. Write a `for` loop.
- The logic needs several steps, `try`/`except`, or more than one `if`. A comprehension that wraps over three lines is harder to read than the loop.
- You'd need to nest more than two levels.

If a colleague has to stop and decode it, the loop was better.

## enumerate and zip

Beginners often write loops over `range(len(...))` to get positions:

```python
runners = ["Ada", "Grace", "Alan"]
for i in range(len(runners)):
    print(i + 1, runners[i])
```

`enumerate` gives you the position and the item together:

```python
for place, name in enumerate(runners, start=1):
    print(place, name)
# 1 Ada
# 2 Grace
# 3 Alan
```

`zip` walks over several sequences **side by side**, giving you one item from each per step:

```python
names = ["Ada", "Grace", "Alan"]
scores = [91, 85, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Ada: 91
# Grace: 85
# Alan: 78

print(dict(zip(names, scores)))   # {'Ada': 91, 'Grace': 85, 'Alan': 78}
```

`zip` stops at the end of the **shortest** sequence, silently. If your lists should be the same length, pass `strict=True` (Python 3.10+) to get a `ValueError` when they aren't, instead of quietly losing data.

## any and all

Checking whether some or every item matches a condition is so common that there are built-ins for it:

```python
scores = [91, 85, 78, 42]

print(any(s < 50 for s in scores))    # True: at least one failed
print(all(s >= 40 for s in scores))   # True: everyone got 40 or more
```

Both stop as soon as they know the answer: `any` at the first `True`, `all` at the first `False`. Note the edge case: `all([])` is `True` and `any([])` is `False`. "Every item in an empty list is positive" is true, because there's no item that isn't.

## Sorting with a key

`sorted` returns a new sorted list and leaves the original alone. `list.sort()` sorts the list **in place** and returns `None`.

```python
words = ["banana", "Apple", "cherry"]
print(sorted(words))   # ['Apple', 'banana', 'cherry']   (capitals sort first)
```

To sort by something other than the items themselves, pass a `key`: a function that's called on each item, and whose result is used for comparing.

```python
print(sorted(words, key=str.lower))   # ['Apple', 'banana', 'cherry']
print(sorted(words, key=len))         # ['Apple', 'banana', 'cherry']
```

### lambda

Often the key is a tiny one-off function. A **lambda** is a function written inline, without a name: `lambda x: x["grade"]` means "a function that takes `x` and returns `x["grade"]`".

```python
students = [
    {"name": "Grace", "grade": 85},
    {"name": "Ada", "grade": 91},
    {"name": "Alan", "grade": 85},
]

by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print([s["name"] for s in by_grade])   # ['Ada', 'Grace', 'Alan']
```

### Sorting by several things

What if two students have the same grade and you want them alphabetical? Make the key return a **tuple**. Tuples compare item by item: first by the first item, and only if those are equal, by the second.

```python
ranked = sorted(students, key=lambda s: (-s["grade"], s["name"]))
print([s["name"] for s in ranked])   # ['Ada', 'Alan', 'Grace']
```

The minus sign sorts grades high-to-low while names stay A-to-Z. (That trick only works for numbers.)

Python's sort is **stable**: items that compare equal keep their original order. That's a guarantee you can rely on, and it's why sorting twice works too: sort by the secondary key first, then by the primary key.

`min` and `max` take a `key` as well:

```python
best = max(students, key=lambda s: s["grade"])
print(best["name"])   # Ada
```

## Generators: values on demand

A list comprehension builds the whole list in memory at once. With a million items that's a million items in memory, even if you only need to add them up. A **generator expression** looks like a comprehension with round brackets, but produces items one at a time, only when asked:

```python
squares = (n * n for n in range(1_000_000))
print(squares)        # <generator object <genexpr> at 0x...>
print(sum(squares))   # 333332833333500000
```

The generator never holds more than one square at a time. When a generator is the only argument to a function you can drop the extra brackets: `sum(n * n for n in range(1_000_000))`.

### yield

You can write your own generator as a function, using `yield` instead of `return`. Each `yield` hands one value to the caller and **pauses** the function right there; the next request resumes it from that line.

```python
def countdown(n):
    print("starting")
    while n > 0:
        yield n
        n -= 1

gen = countdown(3)    # nothing printed yet: the body hasn't started
print(next(gen))      # starting
                      # 3
print(next(gen))      # 2
print(list(gen))      # [1]
```

Calling `countdown(3)` doesn't run the body at all; it creates a generator object. The body only starts at the first `next()` (a `for` loop calls `next()` for you). When the function ends, the generator is exhausted, and asking again gives nothing.

Generators can even be endless, because they never build the whole sequence:

```python
import itertools

def evens():
    n = 0
    while True:
        yield n
        n += 2

print(list(itertools.islice(evens(), 5)))   # [0, 2, 4, 6, 8]
```

`itertools.islice` takes the first few items from any iterable, generators included. Generators show up all over real code: reading huge files line by line, processing data in batches, streaming results from a database. You'll write a batching generator in the practice.

> **Note:** a generator can only be looped over **once**. After that it's empty. If you need the values twice, make a list, or create a fresh generator.

## Readable beats clever

Every tool in this lesson can be overused. A one-line comprehension with three conditions and a nested `zip` may be impressive, but code is read far more often than it's written. Prefer the version a tired colleague understands in five seconds. When in doubt, use a normal loop with a well-named variable.

## Common mistakes

**`list.sort()` returns `None`.** `names = names.sort()` leaves `names` as `None`, and the next line fails with `TypeError: 'NoneType' object is not iterable`. Use `names.sort()` alone, or `names = sorted(names)`.

**Calling the key function.** `sorted(words, key=len())` raises `TypeError: len() takes exactly one argument (0 given)`. Pass the function itself: `key=len`.

**Reusing an exhausted generator.**

```python
squares = (n * n for n in range(3))
print(sum(squares))   # 5
print(sum(squares))   # 0, because it's already used up
```

**Using a comprehension for side effects.** `[db.save(x) for x in items]` works, but it's a loop pretending to be a list. Write the loop.

**Mixing up the filter `if` and the choice `if/else`.** `[x for x in xs if x > 0 else 0]` is a `SyntaxError`. Filtering goes at the end with no `else`; choosing goes at the front: `[x if x > 0 else 0 for x in xs]`.

## Recap

- Comprehensions build lists `[...]`, dicts `{k: v ...}` and sets `{...}` in one expression: `[expression for item in items if condition]`. Use a loop for side effects or complex logic.
- `enumerate` gives positions and items; `zip` walks sequences side by side (`strict=True` to catch length mismatches); `any`/`all` check conditions.
- `sorted(items, key=..., reverse=...)` returns a new list; a tuple key sorts by several things; Python's sort is stable. `lambda` writes a small key function inline.
- Generators (`(... for ...)` or a function with `yield`) produce values one at a time, use little memory, can be endless, and can be consumed only once.
- Readable beats clever.
