# Functions

## Why this matters

Real programs are thousands of lines long, and nobody can hold that in their head at once. **Functions** are how engineers break a big problem into small, named pieces that each do one job, can be tested on their own, and can be reused. Every code exercise in this course asks you to write a function, and every test calls one. The single most common beginner bug in this course, a function that `print`s its answer instead of `return`ing it, is covered here.

## Defining and calling a function

A **function** is a named block of code that you can run whenever you want by **calling** it.

```python
def greet(name):
    message = f"Hello, {name}!"
    return message

print(greet("Ada"))     # Hello, Ada!
print(greet("Grace"))   # Hello, Grace!
```

- `def` starts the **definition**: the function's name, its **parameters** in brackets, and a colon.
- The indented block is the **body**. It doesn't run when Python reads the `def`, only when the function is called.
- `return` hands a value back to whoever called the function, and ends the function immediately.
- `greet("Ada")` is a **call**. Python runs the body with `name` set to `"Ada"`, and the whole call expression becomes the returned value.

Function names follow the same style as variables: lowercase with underscores, and usually a verb that says what it does (`calculate_total`, `is_valid`, `format_price`).

## Parameters and arguments

These two words are often mixed up:

- A **parameter** is the name in the definition: `name` in `def greet(name):`.
- An **argument** is the actual value passed in a call: `"Ada"` in `greet("Ada")`.

A function can have several parameters. Arguments are matched to them **by position**, first to first:

```python
def area(width, height):
    return width * height

print(area(3, 4))   # 12
```

Or **by keyword**, naming the parameter, in which case the order doesn't matter:

```python
print(area(height=4, width=3))   # 12
```

Keyword arguments make calls easier to read when there are several numbers or `True`/`False` flags.

## `return` vs `print`

This is the most important idea in the lesson.

- `print` **shows** a value on the screen, for a human to read. The program can't use it.
- `return` **gives** a value back to the code that called the function, so it can be stored, compared, or passed to another function.

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)    # shows 5 on screen...
print(x)               # None   ...but gives back nothing

y = add_return(2, 3)   # shows nothing
print(y)               # 5
print(y * 10)          # 50     the value can be used
```

A function without a `return` statement (or with a bare `return`) gives back **`None`**. So when you see `None` where you expected a value, the first thing to check is "did my function return, or did it print?"

The tests in this course call your functions and check what they **return**. A function that prints the right answer still fails. As a rule: functions that compute things should return the result, and only the outermost part of the program (the part that talks to the user) should print.

`return` also ends the function, which makes early exits easy:

```python
def safe_divide(a, b):
    if b == 0:
        return None      # leave now; the line below never runs
    return a / b

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # None
```

## Default arguments

A parameter can have a **default value**, used when the caller doesn't provide that argument:

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))      # 25    exponent defaults to 2
print(power(5, 3))   # 125
```

Parameters with defaults must come after those without. Defaults are perfect for options that are usually the same.

## Keyword-only arguments

Look at this call: `make_label("Ada", True, False)`. What do `True` and `False` mean? You'd have to open the function to find out. Python lets a function **require** some arguments to be passed by name. Put a bare `*` in the parameter list; everything after it is **keyword-only**:

```python
def make_label(name, *, uppercase=False, prefix=""):
    label = f"{prefix}{name}"
    if uppercase:
        label = label.upper()
    return label

print(make_label("Ada", uppercase=True))   # ADA
print(make_label("Ada", prefix="Dr "))      # Dr Ada
make_label("Ada", True)
# TypeError: make_label() takes 1 positional argument but 2 were given
```

The error is the point: the caller is forced to write `uppercase=True`, which reads clearly. Use keyword-only arguments for flags and options.

## Scope: where names exist

Variables created inside a function are **local**: they exist only while that function runs, and only inside it.

```python
def double(n):
    result = n * 2
    return result

print(double(4))   # 8
print(result)
# NameError: name 'result' is not defined
```

Variables created at the top level of the file are **global**: they're visible everywhere in the file, including inside functions. But assigning to a name inside a function creates a *new local* name, even if a global has the same name:

```python
count = 0

def add_one():
    count = 1          # a new local variable; the global count is untouched
    return count

add_one()
print(count)   # 0
```

That's deliberate: a function can't accidentally change variables elsewhere in your program. The clean way to get information in and out of a function is through its **parameters** and its **return value**. Python has a `global` keyword to change a global from inside a function, but you'll rarely need it, and in this course you won't.

## Pure functions and side effects

A **pure function** depends only on its arguments and does nothing except return a value. Same input, same output, every time:

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32
```

A **side effect** is anything a function does besides returning a value: printing, reading input, writing a file, changing a list it was given, sending an email. Programs need side effects (otherwise they'd do nothing visible), but pure functions are far easier to test and reason about: you call them, check the result, done.

A good design habit: keep the calculations in pure functions, and keep the side effects (`input`, `print`, files) in a thin layer around them. That's why the exercises say "return" and the `__main__` block does the printing.

## Docstrings

A **docstring** is a string written as the first line of a function's body. It explains what the function does, for anyone (including you, in a month) who uses it:

```python
def bmi(weight_kg, height_m):
    """Return body-mass index: weight in kg divided by height in metres squared."""
    return weight_kg / height_m ** 2

help(bmi)
# Help on function bmi ...
#     Return body-mass index: weight in kg divided by height in metres squared.
```

Say what goes in and what comes out. Editors show docstrings when you hover over a call.

## Type hints

You'll see signatures like this in every exercise:

```python
def split_bill(total: float, people: int, tip_percent: float) -> float:
```

The `: float` after a parameter and `-> float` after the brackets are **type hints**. They document what types the function expects and returns. Python itself doesn't enforce them at run time, but editors and tools use them to catch mistakes, and they make code much easier to read. `str | None` means "a string or `None`".

## Breaking a problem into functions

Faced with a bigger task, don't write one long block. Split it into steps, and make each step a function:

```python
def bmi(weight_kg, height_m):
    return weight_kg / height_m ** 2

def bmi_category(value):
    if value < 18.5:
        return "underweight"
    elif value < 25:
        return "normal"
    elif value < 30:
        return "overweight"
    return "obese"

def bmi_report(weight_kg, height_m):
    value = bmi(weight_kg, height_m)
    return f"BMI {value:.1f} ({bmi_category(value)})"

print(bmi_report(70, 1.75))   # BMI 22.9 (normal)
```

Each function is short, has one job, and can be tested on its own. `bmi_report` reads almost like English because the hard parts have names. A useful guide: if you can't describe what a function does in one sentence without "and", it probably wants to be two functions.

## Common mistakes

**Printing instead of returning.** The caller gets `None`, and you'll see errors like:

```
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

Read it as: "something was `None` where a number was needed". Find which function should have returned.

**Calling a function before it's defined.** Python runs top to bottom, so the `def` must have run before the call. `NameError: name 'greet' is not defined` at a call usually means this, or a typo.

**Forgetting the brackets.** `print(greet)` shows `<function greet at 0x...>`: the function itself, not its result. Call it: `greet("Ada")`.

**Wrong number of arguments.**

```
TypeError: area() missing 1 required positional argument: 'height'
```

The message names the missing parameter. Check the call against the definition.

**Code after `return` that never runs.** `return` ends the function. Anything after it in the same block is dead code.

**Changing a global from inside a function** and wondering why it didn't change. Return the new value instead.

## Recap

- `def name(parameters):` defines a function; `name(arguments)` calls it. The body runs only when called.
- **Return** values for code to use; **print** only to show people. No `return` means the function gives back `None`.
- Arguments go by position or by keyword. Parameters can have **defaults**. A bare `*` makes the following parameters **keyword-only**.
- Variables inside a function are **local**. Pass data in through parameters and out through `return`.
- Prefer **pure functions** for logic; keep side effects at the edges. Document with **docstrings** and **type hints**.
- Break problems into small functions, each with one job.
