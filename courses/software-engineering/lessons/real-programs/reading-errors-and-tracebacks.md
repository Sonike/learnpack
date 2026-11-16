# Reading errors and tracebacks

Every programmer sees error messages all day, every day. The difference between a beginner and a working engineer isn't that the engineer makes fewer mistakes; it's that they read the error, understand it in seconds, and go straight to the broken line. That skill is learnable, and it starts with not panicking at a wall of red text.

> **Note:** AI assistants are very good at explaining error messages, and that's a fine use for them. But research on engineers learning new code found the biggest drop in skill among people who handed their **debugging** to AI. Read the error yourself first. Ask for an explanation only after you've made a guess.

## Three kinds of mistakes

Code can go wrong in three different ways, and each one shows up differently.

**1. Syntax errors.** The code isn't valid Python, so Python refuses to run any of it. A missing colon, an unclosed bracket, wrong indentation.

```python
def greet(name)
    print("Hello", name)
```

```
  File "greet.py", line 1
    def greet(name)
                   ^
SyntaxError: expected ':'
```

Nothing ran, not even the lines before the mistake. Python points a `^` at where it got confused. The real mistake is usually at that spot or just before it (an unclosed bracket on the previous line is a classic).

**2. Runtime exceptions.** The code is valid Python, it starts running, and then something impossible happens: dividing by zero, looking up a key that isn't there, adding a number to a string. Python stops and raises an **exception**, an object that describes what went wrong. If nothing catches it, the program crashes and prints a traceback.

**3. Logic bugs.** The code runs to the end without any error and gives the wrong answer. These are the hardest, because Python can't tell you about them: as far as Python knows, everything is fine. Debugging them is the topic of the lesson "Debugging systematically". Tests are your best defence.

This lesson is about the first two, and mostly about the second.

## Anatomy of a traceback

Here is a small program with a bug:

```python
# shop.py
prices = {"apple": 0.5, "bread": 2.2}

def line_cost(item, qty):
    return prices[item] * qty

def total(cart):
    result = 0
    for item, qty in cart:
        result += line_cost(item, qty)
    return result

cart = [("apple", 4), ("banana", 2)]
print(total(cart))
```

Run it and Python prints:

```
Traceback (most recent call last):
  File "shop.py", line 14, in <module>
    print(total(cart))
          ~~~~~^^^^^^
  File "shop.py", line 10, in total
    result += line_cost(item, qty)
              ~~~~~~~~~^^^^^^^^^^^
  File "shop.py", line 5, in line_cost
    return prices[item] * qty
           ~~~~~~^^^^^^
KeyError: 'banana'
```

A **traceback** is the list of function calls that were in progress when the error happened. Python prints them oldest first, which is why the header says "most recent call last". So **read it from the bottom up**:

1. **The last line** is the exception's **type** and **message**: `KeyError: 'banana'`. This is the single most important line. A `KeyError` means a dictionary lookup failed, and the message tells you the missing key.
2. **The frame just above it** is where the error actually happened: `File "shop.py", line 5, in line_cost`, plus a copy of that line with `^^^^` markers under the exact part that failed (`prices[item]`).
3. **The frames further up** show how the program got there: line 14 called `total`, which called `line_cost` on line 10.

Each `File ..., line N, in name` block is called a **frame**: one function call that was in progress.

Now you can reason about it: `line_cost` was asked about `"banana"`, and `prices` has no banana. The fix is either to add banana to `prices`, or to decide what should happen for unknown items, for example `prices.get(item, 0)`.

> **Try it:** in the practice editor, write a dict with two keys and look up a third one. Read the traceback bottom-up, then fix it with `.get()`.

### Your code versus library code

In real projects, a traceback often runs through code you didn't write: a library, or Python's own standard library. The rule is: **find the lowest frame that's in your own code**. That's almost always where the mistake is, even if the exception was raised deeper inside a library.

```
Traceback (most recent call last):
  File "/home/ada/report/main.py", line 9, in <module>
    data = json.loads(text)
  File "/usr/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3.12/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

The bug isn't in `json/decoder.py`; the standard library is very well tested. The lowest frame from your project is `main.py` line 9, which passed `text` to `json.loads`. The message says the very first character wasn't valid JSON, so `text` was probably empty or wasn't JSON at all. Your next step is to look at what `text` contains.

## The ten exceptions you'll meet most

You don't need to memorise the whole list in the Python docs. These ten cover most of what you'll see as a beginner.

| Exception | What it means | Typical cause |
|---|---|---|
| `NameError` | A name isn't defined | A typo (`pirnt`), or using a variable before assigning it |
| `TypeError` | An operation got the wrong type of value | `"Age: " + 30`, calling a function with too many arguments |
| `ValueError` | Right type, wrong value | `int("abc")` |
| `KeyError` | A dict has no such key | `prices["banana"]` |
| `IndexError` | A list has no such position | `items[len(items)]` |
| `AttributeError` | The object has no such attribute or method | `None.upper()`, `"hi".push("!")` |
| `ZeroDivisionError` | Division or modulo by zero | an empty list's average |
| `FileNotFoundError` | No file at that path | Wrong folder, wrong name |
| `ImportError` / `ModuleNotFoundError` | An import failed | A package not installed in the active environment |
| `RecursionError` | A function called itself too deeply | A recursive function with no working base case |

Let's see a few in action and practise reading the message.

```python
age = 30
print("Age: " + age)
# TypeError: can only concatenate str (not "int") to str
```

The message tells you exactly what happened: `+` with a string on the left only works if the right side is a string too. Fix it with an f-string, `f"Age: {age}"`, or `str(age)`.

```python
scores = [70, 85, 90]
print(scores[3])
# IndexError: list index out of range
```

A list of 3 items has indexes 0, 1 and 2. Index 3 is one past the end: an **off-by-one error**, one of the most common bugs in all of programming. It often hides in loops like `for i in range(len(scores)): scores[i + 1]`.

```python
name = None
print(name.upper())
# AttributeError: 'NoneType' object has no attribute 'upper'
```

When you see `'NoneType' object has no attribute ...`, the question isn't "why doesn't None have `upper`?" but "**why is this variable `None`**?" The usual answer: a function that forgot to `return` something, so it returned `None` by default.

```python
def average(xs):
    return sum(xs) / len(xs)

print(average([]))
# ZeroDivisionError: division by zero
```

The code is fine for normal lists and crashes on an empty one. Empty inputs are such a common source of crashes that you should always ask "what if it's empty?" when you write a function.

```python
import requets
# ModuleNotFoundError: No module named 'requets'
```

Either a typo (here: `requests`), or the package isn't installed in the Python environment you're running. The lesson "Modules, packages and the standard library" covers environments.

## Chained tracebacks

Sometimes you'll see two tracebacks in a row, joined by this sentence:

```
During handling of the above exception, another exception occurred:
```

It means code was handling the first error (in an `except` block, covered in the lesson "Handling exceptions") and a second error happened. **The last traceback is the one that crashed your program**, so start there; the first one tells you what was going on when things went wrong. A similar message, `The above exception was the direct cause of the following exception`, appears when code deliberately raised a new error *from* the old one to add context.

## How to read any error: a routine

1. **Read the last line.** Exception type, then message. Say it out loud in plain English: "a dictionary didn't have the key 'banana'".
2. **Find the lowest frame in your own code.** Open that file at that line.
3. **Look at the values involved on that line.** Which one could be wrong? Print it if you're not sure (`print(repr(item))` shows quotes and hidden spaces).
4. **Ask why it has that value.** Follow it back up the frames if needed.
5. **Fix, then re-run** to confirm the error is gone and nothing new broke.

### Searching an error message well

If you're stuck after reading carefully, search. Good search habits:

- Copy the **type and the general part of the message**, and leave out what's specific to you: search `TypeError: can only concatenate str (not "int") to str`, not your variable names or file paths.
- Add the language or library: `python json.decoder.JSONDecodeError Expecting value`.
- Prefer results from the official docs and from Stack Overflow answers with an explanation, not just code. Check the date: answers about Python 2 are often wrong now.
- Understand the fix before you paste it. If you can't explain why it works, you haven't fixed the bug, you've hidden it.

## Common mistakes

**Reading the traceback from the top.** The first frame is usually the line in your main script that started everything, which is rarely where the problem is. Bottom first.

**Blaming the line Python points to for a syntax error.** With a missing `)` or `]`, Python often only notices on the *next* line:

```python
total = sum([1, 2, 3)
print(total)
```

```
  File "sum.py", line 1
    total = sum([1, 2, 3)
                        ^
SyntaxError: closing parenthesis ')' does not match opening parenthesis '['
```

Recent Python versions are good at pinpointing this, but if the line it points at looks fine, check the line above.

**Fixing the symptom instead of the cause.** A `KeyError` can be "fixed" by wrapping the line in `try/except` and ignoring the error. Now the program runs and silently gives wrong totals, which is worse than crashing. First ask: *should* that key be there? If yes, find out why it isn't. If missing keys are normal, decide deliberately what they mean (`.get(item, 0)`).

**Ignoring the message.** `TypeError: greet() takes 1 positional argument but 2 were given` tells you the function name, how many arguments it expects and how many you passed. Messages are written by people who've seen this mistake a thousand times. Read every word.

## Recap

- Syntax errors stop the program before it starts; exceptions stop it while running; logic bugs don't stop it at all.
- A traceback lists the calls that were in progress, oldest first. Read it **bottom-up**: exception type and message, then the innermost frame, then the call chain.
- In a traceback through library code, look for the **lowest frame in your own code**.
- Learn the ten common exceptions; each one points to a short list of likely causes.
- When searching, use the generic part of the message, and understand a fix before you use it.
