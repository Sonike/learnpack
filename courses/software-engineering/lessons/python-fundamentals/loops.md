# Loops

## Why this matters

Computers are worth having because they repeat work without getting bored: check every order, send every email, total every row of a spreadsheet. A **loop** is how you tell a program to repeat. Two loop bugs are so common they have names, the **off-by-one error** and the **infinite loop**, and nearly every working programmer has shipped at least one of each. This lesson shows you the patterns that work and how to spot those two before they bite.

## `for` loops: do something for each item

A `for` loop runs its block once for every item in a sequence, with a variable set to the current item each time:

```python
for name in ["Ada", "Grace", "Linus"]:
    print(f"Hello, {name}!")
# Hello, Ada!
# Hello, Grace!
# Hello, Linus!
```

The loop variable (`name`) is a normal variable. Python makes it refer to the first item, runs the indented block, then makes it refer to the next item, and so on until there are no items left.

Strings are sequences of characters, so you can loop over them too:

```python
for ch in "hey":
    print(ch)
# h
# e
# y
```

## `range`: counting

To repeat something a number of times, or to loop over numbers, use `range`:

```python
for i in range(5):
    print(i, end=" ")
# 0 1 2 3 4
```

(`end=" "` tells `print` to end with a space instead of a new line, to keep the output short.)

`range` has three forms, and the most important fact about it is that **the stop value is not included**:

```python
range(5)          # 0, 1, 2, 3, 4           stop at 5 (not included)
range(1, 6)       # 1, 2, 3, 4, 5           start at 1, stop before 6
range(2, 10, 3)   # 2, 5, 8                 start 2, step 3, stop before 10
range(10, 0, -2)  # 10, 8, 6, 4, 2          counting down
```

`range(n)` runs exactly `n` times, which is why it starts at 0. To count from 1 to `n` inclusive, write `range(1, n + 1)`.

You can see what a `range` contains by turning it into a list: `print(list(range(2, 10, 3)))` shows `[2, 5, 8]`.

## The accumulator pattern

The most common loop of all: start a variable at an "empty" value, then update it with each item.

```python
prices = [4.50, 2.25, 10.00]
total = 0                  # 1. start empty
for price in prices:
    total += price         # 2. update with each item
print(total)               # 3. use the result: 16.75
```

The same shape builds a string or a list:

```python
shout = ""
for ch in "hey":
    shout += ch.upper() + "!"
print(shout)   # H!E!Y!

squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)   # [1, 4, 9, 16, 25]
```

A **counter** is an accumulator that adds 1 when something is true:

```python
words = ["apple", "kiwi", "banana", "fig"]
long_words = 0
for word in words:
    if len(word) > 4:
        long_words += 1
print(long_words)   # 2
```

Put the starting value **before** the loop. If you write `total = 0` inside the loop, it resets on every pass.

## `while` loops: repeat until something changes

A `while` loop repeats as long as a condition is true. Use it when you don't know in advance how many times you'll go round:

```python
balance = 100
years = 0
while balance < 200:
    balance = balance * 1.07   # 7% growth a year
    years += 1
print(years)   # 11
```

Python checks the condition, runs the block, checks again, and stops the first time the condition is false. Something inside the loop **must** change the condition eventually. Here `balance` grows each time.

You can also use `while` to take a number apart digit by digit, using `%` and `//` from "Values, variables and types":

```python
n = 4096
digits = 0
while n > 0:
    n = n // 10    # drop the last digit
    digits += 1
print(digits)   # 4
```

> **Try it:** change the code above to add up the digits instead of counting them. `n % 10` is the last digit. You'll need that in the first exercise.

## `break` and `continue`

- **`break`** leaves the loop immediately.
- **`continue`** skips the rest of this pass and goes on to the next item.

```python
for n in [3, 8, -1, 5]:
    if n < 0:
        print("negative found, stopping")
        break
    print(n)
# 3
# 8
# negative found, stopping

for word in ["ok", "", "fine", ""]:
    if not word:
        continue        # skip empty words
    print(word)
# ok
# fine
```

`break` is ideal for searching: once you've found what you want, stop looking. A function can do the same with `return`, which ends both the loop and the function, as you'll see in "Functions".

## Looping with an index: `enumerate`

Sometimes you need the position as well as the item. Don't count by hand; use `enumerate`:

```python
for i, name in enumerate(["Ada", "Grace", "Linus"]):
    print(i, name)
# 0 Ada
# 1 Grace
# 2 Linus
```

`enumerate(items, start=1)` numbers from 1 instead, handy for showing numbered lists to people.

## Off-by-one errors

An **off-by-one error** is a loop that runs one time too many or one too few. It almost always comes from a boundary: `<` vs `<=`, or `range(n)` vs `range(n + 1)`.

```python
# Goal: add up 1 + 2 + ... + 10 (the answer is 55)
total = 0
for n in range(1, 10):     # bug: stops at 9
    total += n
print(total)   # 45
```

`range(1, 10)` stops *before* 10. The fix is `range(1, 11)`. The way to catch these: test the boundary by hand. "Does my loop include the first item? The last? What happens with 0 items? With 1?"

The √n trick in this lesson's prime-number exercise is a good example. To test if `n` is prime, you only need to try divisors `d` while `d * d <= n`. With `<` instead of `<=`, the number 49 (= 7 × 7) never gets tested against 7 and looks prime. One character, wrong answer.

## Infinite loops and Ctrl+C

A `while` loop whose condition never becomes false runs forever:

```python
count = 0
while count < 5:
    print(count)
    # forgot: count += 1
```

This prints `0` over and over. The program isn't crashed; it's doing exactly what you said. Stop it with **Ctrl+C** in the terminal. You'll see:

```
KeyboardInterrupt
```

That's Python reporting that you interrupted it, not a bug in your code. In the practice editor, use the Stop button.

When you write a `while` loop, ask two questions: "what makes the condition false?" and "does every pass move towards that?"

> **Note:** some processes have no known guarantee of stopping. The Collatz exercise in this lesson is one: nobody has proved the loop ends for every starting number, though it has for every number ever tried. It's a fun reminder that "will this loop finish?" can be a hard question.

## Seeing a loop run

When a loop surprises you, stop guessing and watch it. Two ways:

1. **Print inside the loop**, showing the variables you care about:

   ```python
   total = 0
   for n in range(1, 4):
       total += n
       print(f"n={n} total={total}")
   # n=1 total=1
   # n=2 total=3
   # n=3 total=6
   ```

2. **Python Tutor** (linked below) steps through your code one line at a time and draws every variable. It's the best way to build an intuition for loops.

## Common mistakes

**Forgetting the colon or indentation** gives `SyntaxError: expected ':'` or `IndentationError`, just like `if`.

**Resetting the accumulator inside the loop.**

```python
for price in prices:
    total = 0          # wrong place: reset every pass
    total += price
```

**Changing a list while looping over it.** Removing items from a list inside `for item in that_list:` skips items, because the positions shift under the loop. Build a new list instead.

**`range(len(items))` when you only need the items.** `for i in range(len(names)): print(names[i])` works but is harder to read than `for name in names:`. Use `enumerate` when you need both.

**An infinite loop because the variable never changes**, or changes in the wrong direction (`n += 1` when the condition waits for `n` to reach 0).

**Off-by-one in `range`.** Remember: the stop value is never included.

## Recap

- `for item in sequence:` runs the block once per item. `range(start, stop, step)` produces numbers and **never includes stop**.
- The **accumulator** pattern: start empty before the loop, update inside it, use it after. A **counter** adds 1 when a condition is true.
- `while condition:` repeats until the condition is false. Something inside must change it.
- `break` leaves the loop; `continue` skips to the next pass. `enumerate` gives you the index and the item.
- **Off-by-one errors** come from boundaries; test the first, last, empty and single-item cases.
- An **infinite loop** is stopped with **Ctrl+C**. Print inside the loop or use Python Tutor to see what's happening.
