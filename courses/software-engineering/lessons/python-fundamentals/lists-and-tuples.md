# Lists and tuples

## Why this matters

Real data comes in collections: the items in a basket, the rows of a spreadsheet, the lines of a log file, the moves in a game. A **list** is Python's everyday way to hold many values in order. Lists are also where beginners meet one of the most confusing bugs in programming: you change one list and another one changes too. Once you understand **aliasing**, that bug stops being spooky, and you'll understand how Python treats every value, not just lists.

## Making a list

A list is written with square brackets, items separated by commas. It can hold any values, even a mix of types:

```python
scores = [72, 95, 88]
names = ["Ada", "Grace", "Linus"]
empty = []
mixed = [1, "two", 3.0, None]

print(len(scores))   # 3     how many items
print(len(empty))    # 0
```

Lists keep their items **in order**, and the same value can appear more than once.

## Indexing: getting one item

Each item has a position called its **index**. Indexes start at **0**:

```
names  =  [ "Ada", "Grace", "Linus" ]
index:       0        1        2
negative:   -3       -2       -1
```

```python
names = ["Ada", "Grace", "Linus"]
print(names[0])    # Ada      the first item
print(names[2])    # Linus
print(names[-1])   # Linus    negative indexes count from the end
print(names[-2])   # Grace
```

So the last item of any non-empty list is `items[-1]`, and the valid indexes for a list of length `n` run from `0` to `n - 1`. Asking for one past the end is an error:

```python
print(names[3])
# IndexError: list index out of range
```

## Slicing: getting a piece

A **slice** `items[start:stop]` gives a **new list** from `start` up to, **but not including**, `stop`. It's the same rule as `range`.

```python
letters = ["a", "b", "c", "d", "e"]
print(letters[1:3])   # ['b', 'c']            indexes 1 and 2
print(letters[:2])    # ['a', 'b']            from the start
print(letters[3:])    # ['d', 'e']            to the end
print(letters[-2:])   # ['d', 'e']            the last two
print(letters[::2])   # ['a', 'c', 'e']       every second item
print(letters[::-1])  # ['e', 'd', 'c', 'b', 'a']   reversed
print(letters[:])     # a full copy
```

Unlike indexing, slicing never raises an error for out-of-range values; `letters[3:100]` just gives what's there.

## Changing a list

Lists are **mutable**: you can change them after creating them.

```python
basket = ["apple", "bread"]
basket.append("milk")          # add to the end
print(basket)                  # ['apple', 'bread', 'milk']
basket.insert(0, "eggs")       # insert at index 0
print(basket)                  # ['eggs', 'apple', 'bread', 'milk']
basket[1] = "pear"             # replace by index
print(basket)                  # ['eggs', 'pear', 'bread', 'milk']
last = basket.pop()            # remove and return the last item
print(last, basket)            # milk ['eggs', 'pear', 'bread']
first = basket.pop(0)          # remove and return the item at index 0
print(first, basket)           # eggs ['pear', 'bread']
basket.remove("bread")         # remove the first item equal to "bread"
print(basket)                  # ['pear']
```

`remove` raises `ValueError: list.remove(x): x not in list` if the value isn't there, and `pop` on an empty list raises `IndexError: pop from empty list`.

## Looping and checking membership

You've already looped over lists in "Loops". Two more tools:

```python
names = ["Ada", "Grace", "Linus"]
print("Grace" in names)        # True
print("Alan" not in names)     # True
print(names.index("Linus"))    # 2   position of the first match
print(sum([3, 4, 5]), max([3, 4, 5]), min([3, 4, 5]))   # 12 5 3
```

## Sorting: `sorted()` vs `.sort()`

There are two ways to sort, and mixing them up is a classic bug.

```python
nums = [3, 1, 2]

new = sorted(nums)     # returns a NEW sorted list; nums is unchanged
print(new, nums)       # [1, 2, 3] [3, 1, 2]

result = nums.sort()   # sorts nums IN PLACE and returns None
print(result, nums)    # None [1, 2, 3]
```

Both accept `reverse=True` for descending order. Rule of thumb: use `sorted()` when you want a sorted copy, `.sort()` when you want to change the list itself. Never write `nums = nums.sort()`; you'd replace your list with `None`.

## Mutability and aliasing: two names, one list

Remember from "Values, variables and types" that a variable is a **label** on a value, not a box. Assignment doesn't copy; it sticks a second label on the **same** value:

```python
a = [1, 2, 3]
b = a            # b is another name for the same list
b.append(4)
print(a)         # [1, 2, 3, 4]   a changed too!
print(a is b)    # True           same object
```

```
a ──┐
    ├──►  [1, 2, 3, 4]      one list, two names
b ──┘
```

This is **aliasing**: two names for one object. With numbers and strings you never notice it, because they can't be changed in place; `x += 1` makes a new number and moves the label. With lists you can change the object itself, so every name that refers to it sees the change.

To get an independent list, make a **copy**:

```python
a = [1, 2, 3]
b = a.copy()     # or list(a), or a[:]
b.append(4)
print(a)         # [1, 2, 3]
print(b)         # [1, 2, 3, 4]
```

The same applies to functions. Passing a list to a function passes the **same list**, so a function that changes its argument changes the caller's list:

```python
def add_bonus(scores):
    scores.append(100)     # changes the caller's list (a side effect)

my_scores = [70, 80]
add_bonus(my_scores)
print(my_scores)   # [70, 80, 100]
```

Sometimes that's what you want. Often it's a surprise for the caller. A safe default is: **don't change lists you were given; build and return a new one.** Several exercises in this lesson test exactly that.

> **Try it:** paste the `a = [1, 2, 3]; b = a; b.append(4)` example into Python Tutor (linked below) and watch both arrows point at one list.

## Tuples and unpacking

A **tuple** is like a list that can't be changed. It's written with round brackets:

```python
point = (3, 4)
print(point[0])    # 3
point[0] = 10
# TypeError: 'tuple' object does not support item assignment
```

Use a tuple for a small, fixed group of values that belong together, like coordinates, an RGB colour, or a function returning two things. Use a list for a collection that grows, shrinks or gets sorted.

**Unpacking** assigns the parts of a tuple (or list) to several names at once:

```python
x, y = (3, 4)
print(x, y)   # 3 4

def min_max(nums):
    return min(nums), max(nums)    # returns a tuple

low, high = min_max([4, 9, 1])
print(low, high)   # 1 9

a, b = 1, 2
a, b = b, a        # swap without a temporary variable
print(a, b)        # 2 1
```

The number of names must match the number of values, or you get `ValueError: too many values to unpack`.

## Nested lists

A list can contain lists. That's a simple way to store a grid, like a spreadsheet or a game board:

```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
]
print(grid[1])       # [4, 5, 6]   the second row
print(grid[1][2])    # 6           row 1, column 2
for row in grid:
    for value in row:
        print(value, end=" ")
# 1 2 3 4 5 6
```

`grid[r][c]` reads as "row `r`, then column `c` within it". The number of rows is `len(grid)`, and the number of columns is `len(grid[0])`.

One trap: `[[0] * 3] * 2` looks like a 2×3 grid of zeros, but it's **two names for the same row** (aliasing again). Change one row and the other changes. Build grids with a loop or `[[0] * 3 for _ in range(2)]` instead.

## Common mistakes

**`IndexError: list index out of range`.** You asked for an index that doesn't exist: often `items[len(items)]` (one past the end) or `items[0]` on an empty list. Check the list's length, and remember the last index is `len(items) - 1`.

**`x = x.sort()`.** `.sort()` returns `None`. Use `x.sort()` on its own line, or `x = sorted(x)`.

**Surprise changes through aliasing.** If a list changes "by itself", look for a `b = a` or a function that modified a list it was given. Copy when you need independence.

**Modifying a list while looping over it.** Removing items inside `for x in items:` skips elements. Loop over a copy (`for x in items[:]:`) or build a new list.

**Forgetting slices exclude the stop index.** `items[1:3]` has two items, not three.

## Recap

- Lists hold values **in order**; `len()` counts them. Indexes start at **0**; `-1` is the last item.
- `items[start:stop]` slices into a **new** list, excluding `stop`. `[::-1]` reverses.
- Lists are **mutable**: `append`, `insert`, `pop`, `remove` and index assignment change them in place.
- `sorted(x)` returns a new list; `x.sort()` changes `x` and returns `None`.
- `b = a` makes an **alias**, not a copy. Use `.copy()` or `[:]` to get an independent list. Functions receive the same list, not a copy.
- **Tuples** are fixed-size and unchangeable; **unpacking** assigns their parts to names. Nested lists make grids: `grid[row][col]`.
