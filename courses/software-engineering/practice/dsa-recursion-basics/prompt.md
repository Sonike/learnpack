# Three recursive functions

Write each one recursively: a **base case** that answers directly, and a **recursive case** that calls the function on a smaller problem.

## 1. Flatten nested lists

```python
def flatten(nested: list) -> list: ...
```

`nested` is a list whose items are either plain values or more lists (nested to any depth). Return one flat list of the plain values, in order. Check `isinstance(item, list)`.

```python
flatten([1, [2, [3, 4]], [], 5])  # [1, 2, 3, 4, 5]
```

## 2. Fast power

```python
def power(base: int, exp: int) -> int: ...
```

Return `base ** exp` for `exp >= 0` **without** using `**` or `pow`. Make it O(log exp) by halving the exponent:

```
power(b, 0) = 1
power(b, e) = half * half            if e is even, where half = power(b, e // 2)
power(b, e) = half * half * b        if e is odd
```

```python
power(2, 10)  # 1024
power(5, 0)   # 1
```

> **Note:** One test calls `power(2, 5000)`. Multiplying one step at a time recursively would need 5000 nested calls and crash with `RecursionError`; halving needs about 13.

## 3. Count grid paths

```python
def count_paths(rows: int, cols: int) -> int: ...
```

A robot starts in the top-left cell of a `rows × cols` grid and wants the bottom-right cell. It may only move **right** or **down**. How many different paths are there? (`rows` and `cols` are at least 1.) From any cell, the paths = paths after moving down + paths after moving right. A grid with one row or one column has exactly 1 path.

```python
count_paths(2, 2)  # 2   (right-down, down-right)
count_paths(3, 3)  # 6
count_paths(1, 7)  # 1
```
