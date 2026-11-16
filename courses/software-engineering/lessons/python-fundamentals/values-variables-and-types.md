# Values, variables and types

## Why this matters

Every program, from a calculator to a bank, is values being stored, combined and shown. A surprising share of real bugs come from the basics in this lesson: a number that was actually text (`"3" + "4"` gives `"34"`), a division that should have been whole-number division, or money that comes out as `0.30000000000000004`. Get these right and the rest of Python is built on solid ground.

## Values and their types

A **value** is a piece of data: `42`, `3.5`, `"hello"`. Every value has a **type**, which decides what you can do with it. Python's basic types:

```python
print(type(42))        # <class 'int'>     a whole number (integer)
print(type(3.5))       # <class 'float'>   a number with a fractional part
print(type("hello"))   # <class 'str'>     text (a string of characters)
print(type(True))      # <class 'bool'>    True or False
print(type(None))      # <class 'NoneType'> "no value"
```

- **`int`**: whole numbers, positive or negative, as big as you like: `7`, `-3`, `10**30`. You can write `1_000_000` with underscores for readability.
- **`float`**: numbers with a decimal point: `3.5`, `-0.25`, `2.0`. The name comes from "floating point", the way the computer stores them.
- **`str`**: text, written inside quotes. `'single'` and `"double"` quotes mean the same thing.
- **`bool`**: only two values, `True` and `False` (capitalised). You'll use them constantly in the next lesson.
- **`None`**: a single special value meaning "nothing here", like an empty box. Functions that don't return anything give back `None`.

Note that `"42"` (in quotes) is a string, not a number. It looks like a number to you; to Python it's two characters.

## Variables are names for values

A **variable** is a name that refers to a value. You create one with `=`, the **assignment** operator:

```python
price = 4
quantity = 3
total = price * quantity
print(total)   # 12
```

Read `=` as "now refers to", not "equals". The right side is worked out first, then the name on the left is attached to the result. So this is perfectly normal:

```python
count = 10
count = count + 1   # take the current value (10), add 1, and make count refer to 11
print(count)        # 11
count += 1          # a shortcut for the same thing
print(count)        # 12
```

A useful picture: a variable is a **label** stuck onto a value, not a box the value lives in. `x = 5` sticks the label `x` on the value 5. `x = 6` moves the label to 6. This picture will matter a lot when we reach lists.

### Naming variables

Names can contain letters, digits and underscores, and can't start with a digit. Python style (called **PEP 8**) uses lowercase words joined by underscores: `total_price`, `user_name`. Names are case-sensitive: `Total` and `total` are different variables.

Choose names that say what the value *means*: `seconds_left` is better than `s` or `x2`. You'll read your code far more often than you write it.

## Arithmetic

```python
print(7 + 2)    # 9
print(7 - 2)    # 5
print(7 * 2)    # 14
print(7 / 2)    # 3.5   true division: always gives a float
print(7 // 2)   # 3     floor division: whole number of times 2 fits into 7
print(7 % 2)    # 1     remainder (called "modulo")
print(7 ** 2)   # 49    power: 7 squared
```

Two of these deserve attention.

**`/` always returns a float**, even when the answer is whole: `6 / 2` is `3.0`, not `3`. If you want a whole number, use `//`.

**`//` and `%` are a pair.** `//` tells you how many whole times one number fits into another, and `%` tells you what's left over. They're how you split a quantity into units:

```python
total_minutes = 135
hours = total_minutes // 60     # 2
minutes = total_minutes % 60    # 15
print(hours, "h", minutes, "min")   # 2 h 15 min
```

`%` also answers "is this divisible?": `n % 2 == 0` means `n` is even. You'll use that in almost every lesson of this section.

Python follows the usual maths order: `**` first, then `*`, `/`, `//`, `%`, then `+` and `-`. Use brackets when in doubt: `(2 + 3) * 4` is 20, `2 + 3 * 4` is 14.

> **Try it:** in the practice editor, print `-7 // 2` and `-7 % 2`. Floor division rounds *down* (towards minus infinity), so the answers might not be what you expect. Predict first.

## Floats are approximate

Run this:

```python
print(0.1 + 0.2)          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # False
```

This isn't a Python bug; almost every programming language does the same. Floats are stored in binary, and just as 1/3 can't be written exactly in decimal (0.3333…), 0.1 can't be written exactly in binary. The stored value is extremely close but not exact, and tiny errors can show up when you add.

What to do about it:

- To **show** a float, format it to the number of places you need (below).
- To **compare** floats, check whether they're close rather than equal: `math.isclose(0.1 + 0.2, 0.3)` is `True`.
- To **round** a value, use `round(x, 2)` for two decimal places.
- For **money** in real systems, store whole cents as `int`s, or use the standard library's `decimal` module. Never trust float equality with money.

## Strings and f-strings

You can join strings with `+` and repeat them with `*`:

```python
first = "Ada"
last = "Lovelace"
print(first + " " + last)   # Ada Lovelace
print("-" * 10)             # ----------
```

The easiest way to build text from values is an **f-string**: put `f` before the opening quote and write any expression inside `{}`:

```python
name = "Ada"
age = 36
print(f"{name} is {age} years old.")   # Ada is 36 years old.
print(f"Next year: {age + 1}")         # Next year: 37
```

After a colon inside the braces you can add a **format spec** that controls how the value looks:

```python
price = 3.14159
print(f"{price:.2f}")       # 3.14       2 decimal places ("f" for fixed-point)
print(f"{price:.1f}")       # 3.1
minutes = 5
print(f"{minutes:02d}")     # 05         at least 2 digits, padded with zeros
print(f"{1234567:,}")       # 1,234,567  thousands separators
```

You'll use `:.1f`, `:.2f` and `:02d` in this lesson's exercises.

## `print()` and `input()`

`print()` shows values. Give it several and it puts spaces between them:

```python
print("Total:", 12, "items")   # Total: 12 items
```

`input()` waits for the user to type a line and press Enter, and gives you what they typed:

```python
name = input("What's your name? ")
print(f"Hi, {name}!")
```

**`input()` always returns a string**, even if the user typed digits. This is the source of the classic bug:

```python
a = input("First number: ")    # user types 3
b = input("Second number: ")   # user types 4
print(a + b)                   # 34   two strings joined, not added
```

> **Note:** the exercises never use `input()`: the tests call your functions directly with values. Keep `input()` for programs you run yourself, like this section's project.

## Converting between types

To turn a value into another type, call the type's name like a function:

```python
print(int("42") + 1)     # 43
print(float("3.5"))      # 3.5
print(str(42) + "!")     # 42!
print(int(3.99))         # 3     int() cuts off the fraction, it doesn't round
print(round(3.99))       # 4
print(bool(0), bool(7))  # False True
```

So the fixed adder is:

```python
a = int(input("First number: "))
b = int(input("Second number: "))
print(a + b)   # 7
```

Conversion fails loudly when the text isn't a valid number:

```python
int("3.5")     # ValueError: invalid literal for int() with base 10: '3.5'
int("ten")     # ValueError: invalid literal for int() with base 10: 'ten'
float("")      # ValueError: could not convert string to float: ''
```

Read the message: a **`ValueError`** means the type was right (a string) but its *value* couldn't be converted. Notice `int("3.5")` fails; use `float()` first if the text might have a decimal point. Handling bad input gracefully, instead of crashing, comes in the next section; for now, know where these errors come from.

## Common mistakes

**Joining a string and a number.**

```python
age = 36
print("Age: " + age)
# TypeError: can only concatenate str (not "int") to str
```

**Concatenate** means "join together". Python won't guess whether you meant text or maths. Use an f-string: `print(f"Age: {age}")`.

**Forgetting that `input()` gives text.** If `+` joins instead of adds, or `>` compares strangely (`"10" < "9"` is `True`, because strings compare letter by letter), convert with `int()` or `float()`.

**Using `/` when you wanted a whole number.** `10 / 2` is `5.0`. If later code needs an `int` (for example, a list index), you'll get `TypeError: list indices must be integers or slices, not float`. Use `//`.

**Testing floats with `==`.** Use `math.isclose`, or round both sides to the precision you care about.

**Rounding too early.** Round once, when you show or store the final result. Rounding each step adds errors: a bill split computed from an already-rounded tip can be a cent off.

**Using a name before assigning it.**

```python
print(totl)
# NameError: name 'totl' is not defined. Did you mean: 'total'?
```

Usually a typo. Python even suggests the name you probably meant.

## Recap

- Basic types: **`int`**, **`float`**, **`str`**, **`bool`** and **`None`**. `type(x)` tells you which.
- A **variable** is a name attached to a value with `=`. The right side is evaluated first.
- `/` always gives a float; `//` is floor division and `%` is the remainder. Together they split quantities into units.
- Floats are approximate: format them for display, compare with `math.isclose`, and round once at the end.
- **f-strings** (`f"{value:.2f}"`) are the clean way to build text.
- `input()` always returns a **string**; convert with `int()`, `float()` or `str()`, and expect a `ValueError` when the text isn't a number.
