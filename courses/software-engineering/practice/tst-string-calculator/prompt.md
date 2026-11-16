# TDD kata: the string calculator

A classic kata for practising test-driven development. Write `add(numbers)` that takes a string of numbers and returns their sum. The requirements come in **five stages**. Work through them in order, TDD style:

1. Read one stage.
2. Add a `check(...)` line for it in the `__main__` block and Run it: it should print `FAIL` (**red**).
3. Write the least code that makes it pass (**green**).
4. Tidy up while everything still passes (**refactor**). Then the next stage.

Don't read ahead and build everything at once. The point is to feel how small steps keep you out of trouble.

```python
def add(numbers: str) -> int: ...
```

**Stage 1.** An empty string returns `0`. One number returns itself. Two numbers separated by a comma return their sum.
```python
add("") == 0;  add("4") == 4;  add("1,2") == 3
```

**Stage 2.** Any amount of numbers.
```python
add("1,2,3,4,5") == 15
```

**Stage 3.** Newlines work as separators too, mixed with commas.
```python
add("1\n2,3") == 6
```

**Stage 4.** A custom delimiter can be set on a first line that looks like `//<delimiter>\n`. The delimiter is a single character. Commas and newlines still work as well.
```python
add("//;\n1;2") == 3;  add("//|\n1|2,3") == 6
```

**Stage 5.** Negative numbers raise `ValueError` with the message `negatives not allowed: ` followed by **all** the negatives, separated by `, `.
```python
add("1,-2,3,-4")   # ValueError: negatives not allowed: -2, -4
```

The hidden tests have one test per stage.

> **Tip:** for stages 3 and 4, a neat move is to turn every separator into a comma with `str.replace`, then `split(",")`.
