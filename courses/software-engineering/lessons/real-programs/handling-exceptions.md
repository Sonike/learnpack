# Handling exceptions

A program that crashes the first time a user types "twelve" instead of "12" isn't finished. Real programs meet bad input, missing files and broken networks every day, and they need a plan for each. Python's plan is exceptions: you **catch** the ones you know how to handle, and you **raise** your own when something is wrong. Doing this well is what separates a script that works on your machine from software other people can rely on.

## try and except

You already know that `int("abc")` raises a `ValueError`. Wrap it in `try`/`except` and you get to decide what happens instead of crashing:

```python
text = "abc"
try:
    number = int(text)
    print("You typed", number)
except ValueError:
    print(f"{text!r} is not a whole number")
# 'abc' is not a whole number
```

How it runs:

1. Python runs the `try` block line by line.
2. If no exception happens, the `except` block is skipped entirely.
3. If an exception happens, Python **stops the `try` block at that line** (so `print("You typed", ...)` never runs) and looks for an `except` clause that matches the exception's type. If one matches, it runs that block and carries on after the whole `try` statement.
4. If none matches, the exception carries on upwards as if there were no `try` at all, and crashes the program with a traceback.

You can get hold of the exception object with `as`, to read its message:

```python
try:
    int("abc")
except ValueError as e:
    print("Problem:", e)
# Problem: invalid literal for int() with base 10: 'abc'
```

## Catch specific exceptions, never everything

You can catch several types with a tuple, or have several `except` clauses:

```python
def read_number(text):
    try:
        return 100 / int(text)
    except ValueError:
        return "not a number"
    except ZeroDivisionError:
        return "can't be zero"

print(read_number("4"))    # 25.0
print(read_number("x"))    # not a number
print(read_number("0"))    # can't be zero
```

What you should **not** do is this:

```python
try:
    result = process(data)
except:          # a "bare except": catches absolutely everything
    pass
```

A bare `except:` (and its cousin `except Exception:` with nothing but `pass` inside) catches every error, including ones you never imagined: a typo in a variable name (`NameError`), a bug in `process`, even the user pressing Ctrl+C. Your program carries on with wrong or missing data, and you have no idea why. This is called **swallowing errors**, and it turns a five-minute bug into a five-day one.

The rule: **catch only the exceptions you expect and know how to handle.** Let everything else crash loudly, with a traceback that tells you exactly where.

### Order matters

Exceptions form a family tree. `ZeroDivisionError` is a kind of `ArithmeticError`, which is a kind of `Exception`. An `except` clause catches its type **and every type below it** in the tree, and Python checks the clauses top to bottom. So a general clause placed first hides the specific ones after it:

```python
try:
    1 / 0
except Exception:
    print("something went wrong")      # this runs
except ZeroDivisionError:
    print("divided by zero")           # never reached
```

Always put the most specific exceptions first.

## else and finally

A full `try` statement has two more optional parts.

```python
try:
    number = int(text)
except ValueError:
    print("not a number")
else:
    print("got", number)          # runs only if the try block raised nothing
finally:
    print("done checking")        # always runs, error or not
```

**`else`** runs only when the `try` block finished without an exception. Why not just put that code at the end of the `try` block? Because then an exception raised by *that* code would be caught by your `except` clause too, and you'd report the wrong problem. Keep the `try` block as small as possible: only the lines that can raise the exception you're catching.

**`finally`** runs no matter what: after success, after a caught exception, even when an uncaught exception is on its way up to crash the program, or when the `try` block executes `return`. It's for **clean-up** that must happen, like closing a connection or deleting a temporary file:

```python
def risky():
    try:
        return 1 / 0
    finally:
        print("cleaning up")

risky()
# cleaning up
# Traceback (most recent call last):
#   ...
# ZeroDivisionError: division by zero
```

The clean-up ran, and then the error carried on. You'll rarely write `finally` for files, because the `with` statement (in the lesson "Files, JSON and CSV") does that clean-up for you.

## Raising your own exceptions

Catching is half of the story. When *your* function receives something it can't work with, it should **raise** an exception, with a message that helps whoever called it.

```python
def set_volume(level):
    if not 0 <= level <= 10:
        raise ValueError(f"volume must be between 0 and 10, got {level}")
    print("Volume set to", level)

set_volume(7)     # Volume set to 7
set_volume(15)    # ValueError: volume must be between 0 and 10, got 15
```

A good error message says **what was expected and what was received**. Compare these:

```
ValueError: invalid input
ValueError: volume must be between 0 and 10, got 15
```

The second one lets someone fix their mistake without opening your code.

Pick the built-in type that fits: `ValueError` for a value that's the right type but not acceptable, `TypeError` for the wrong type entirely, `KeyError`/`LookupError` for something not found.

### Re-raising with context

Sometimes you catch a low-level error and want to raise a clearer one. Use `raise ... from ...`:

```python
import json

def load_config(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError("config file is not valid JSON") from e
```

`from e` keeps the original error attached, so the traceback shows both ("The above exception was the direct cause of the following exception"). Use `from None` when the original adds nothing for the reader, for example when you've already described the problem fully in your own message.

## Custom exception classes

For errors that belong to your program's own world (a bank, a shop, a booking system), define your own exception type. It's a class that inherits from `Exception`; even an empty one is useful:

```python
class OutOfStock(Exception):
    """Raised when an order asks for more than we have."""

def reserve(stock, item, qty):
    available = stock.get(item, 0)
    if qty > available:
        raise OutOfStock(f"only {available} {item} left, {qty} requested")
    stock[item] = available - qty

stock = {"mug": 2}
try:
    reserve(stock, "mug", 5)
except OutOfStock as e:
    print("Sorry:", e)
# Sorry: only 2 mug left, 5 requested
```

Why bother, when `ValueError` exists? Because callers can now catch **exactly this situation** and nothing else. `except ValueError` might also catch a typo-triggered `ValueError` from somewhere unrelated; `except OutOfStock` can't. Your custom exceptions can also carry data as attributes, which you'll do in the practice exercise. Classes are covered properly in the section on objects and clean code; for now, `class Name(Exception):` plus a docstring is all you need.

## Validate at the boundary

Where should all this checking happen? Not everywhere. Data enters your program at a few **boundaries**: user input, files, network requests, command-line arguments. Check it there, once, and convert it to clean, correct values. Code further inside can then trust what it receives.

```python
def parse_quantity(text: str) -> int:
    """Turn user input into a positive int, or raise ValueError."""
    try:
        qty = int(text.strip())
    except ValueError:
        raise ValueError(f"quantity must be a whole number, got {text!r}") from None
    if qty < 1:
        raise ValueError(f"quantity must be at least 1, got {qty}")
    return qty
```

The code that asks the user handles the error by asking again; everything after `parse_quantity` knows `qty` is a positive `int`.

```python
while True:
    try:
        qty = parse_quantity(input("How many? "))
        break
    except ValueError as e:
        print(e)
```

## Fail loudly or recover?

When should you catch an error, and when should you let it crash? A useful test: **can this code do something sensible about it?**

- A user typed a bad value? Yes: show a message and ask again.
- One row in a 10,000-row import is broken? Often yes: record the problem, skip the row, and report all failures at the end (you'll write this in the practice).
- A config file your program can't run without is missing? No sensible fallback exists, so **fail loudly**: stop with a clear message. Silently carrying on with half a config causes stranger failures later.
- An error you didn't expect at all? Don't catch it. Let the traceback tell you about the bug.

"Errors should never pass silently, unless explicitly silenced," as *The Zen of Python* puts it (type `import this` in a Python shell to read the rest).

## Common mistakes

**Catching too much in the try block.**

```python
try:
    age = int(text)
    category = categorise(age)    # a bug in here raising ValueError...
except ValueError:
    print("Please type a number") # ...is reported as bad input
```

Only wrap the line that can raise what you're catching, and use `else` for the rest.

**Catching and printing, then carrying on with garbage.**

```python
try:
    price = float(row["price"])
except ValueError:
    print("bad price")
total += price      # NameError, or worse: last row's price used again
```

After an `except`, make sure the code that follows still makes sense: `continue` to the next row, return early, or set a deliberate default.

**Raising the wrong thing.** `raise "something broke"` gives `TypeError: exceptions must derive from BaseException`. You raise exception objects (or classes): `raise ValueError("something broke")`.

**Using exceptions as a vague "return False".** If a function's normal job includes "not found" (like looking up an optional setting), returning `None` or a default is often clearer than raising. Raise for situations the caller must not ignore.

## Recap

- `try`/`except` lets you handle exceptions you expect. Catch **specific** types, most specific first. Never use a bare `except:`.
- `else` runs when nothing went wrong; `finally` always runs and is for clean-up.
- `raise ValueError("what was expected, what was received")` when your function can't work with its input. Use `raise ... from e` to add context.
- Custom exceptions (`class OutOfStock(Exception)`) let callers catch exactly your domain's problems.
- Validate data at the boundary, recover when you have a sensible plan, and otherwise fail loudly.
