# Conditionals and boolean logic

## Why this matters

Programs become useful when they make decisions: let this user in or not, charge shipping or not, show an error or carry on. Every decision is a condition that comes out `True` or `False`. Most bugs in decision code aren't in the common case; they're at the edges: the score of exactly 90, the empty list, the year 1900. Learning to write conditions clearly, and to test their edges on purpose, is a habit you'll use every day as an engineer.

## Comparisons give booleans

A **comparison** asks a yes/no question and answers with a `bool`:

```python
age = 17
print(age >= 18)    # False
print(age < 18)     # True
print(age == 17)    # True    == asks "are these equal?"
print(age != 17)    # False   != asks "are these different?"
```

The six comparison operators are `==`, `!=`, `<`, `<=`, `>` and `>=`. Note the difference between `=` (assignment: "make this name refer to that value") and `==` (comparison: "are these equal?"). Mixing them up is a classic mistake, and Python helps by refusing `if age = 18:` with a `SyntaxError`.

Python lets you chain comparisons the way you'd write them in maths:

```python
score = 85
print(80 <= score < 90)   # True   same as (80 <= score) and (score < 90)
```

Strings compare too: `==` checks they're exactly the same (capitals matter: `"Ada" == "ada"` is `False`), and `<` compares them alphabetically, character by character.

## `and`, `or`, `not`

Combine conditions with three **boolean operators**:

- `a and b` is `True` only when **both** are `True`.
- `a or b` is `True` when **at least one** is `True`.
- `not a` flips `True` to `False` and back.

```python
age = 25
has_ticket = True
print(age >= 18 and has_ticket)   # True
print(age < 12 or age >= 65)      # False   (not a child, not a senior)
print(not has_ticket)             # False
```

When you mix them, `not` is applied first, then `and`, then `or`, just as `*` comes before `+`. So `a or b and c` means `a or (b and c)`. Don't make readers remember that: **add brackets** whenever you mix `and` and `or`.

`and` and `or` also **short-circuit**: they stop as soon as the answer is known. In `a and b`, if `a` is `False`, `b` is never even evaluated. That lets you guard a risky check:

```python
items = []
if len(items) > 0 and items[0] == "start":   # items[0] is only looked at if the list isn't empty
    print("starts with start")
```

## `if`, `elif`, `else`

An **`if` statement** runs a block of code only when a condition is `True`:

```python
temperature = 31
if temperature > 30:
    print("It's hot.")
    print("Drink water.")
print("Done.")
# It's hot.
# Drink water.
# Done.
```

The **indented** lines (four spaces) after the colon form the **block**. Indentation is how Python knows which lines belong to the `if`; `print("Done.")` isn't indented, so it always runs.

Add `else` for the "otherwise" case, and `elif` (short for "else if") for more options. Python checks each condition **top to bottom** and runs **only the first** block whose condition is true:

```python
temperature = 18
if temperature > 30:
    print("hot")
elif temperature > 15:
    print("mild")
elif temperature > 5:
    print("cool")
else:
    print("cold")
# mild
```

18 is also greater than 5, but once `mild` matched, the rest is skipped. That's why **order matters**. If you put `temperature > 5` first, everything above 5 would print `cool`.

```
           ┌─────────────┐  yes
           │ temp > 30 ? ├──────► "hot"
           └──────┬──────┘
                  │ no
           ┌──────▼──────┐  yes
           │ temp > 15 ? ├──────► "mild"
           └──────┬──────┘
                  │ no
           ┌──────▼──────┐  yes
           │ temp > 5 ?  ├──────► "cool"
           └──────┬──────┘
                  │ no
                  ▼
               "cold"
```

## Truthiness

An `if` doesn't need an actual `bool`. Python treats any value as "truthy" or "falsy". The **falsy** values are:

```
False   None   0   0.0   ""   []   {}   set()   (and other empty collections)
```

Everything else is **truthy**, including `"0"`, `"False"`, `" "` and `[0]`, because they're non-empty. You can check with `bool()`:

```python
print(bool(""))      # False   empty string
print(bool("0"))     # True    a string with one character in it
print(bool([]))      # False   empty list
print(bool([0]))     # True    a list with one item
print(bool(None))    # False
```

This gives you a short, idiomatic way to ask "is there anything here?":

```python
name = input("Name: ").strip()
if not name:
    print("Please enter a name.")
```

Be careful when `0` is a valid value. `if score:` is `False` for a score of 0, which is probably not what you meant. Write `if score is not None:` when you mean "was a score given?".

## Nested vs flat conditions

You can put an `if` inside another `if`, but deep nesting gets hard to read fast:

```python
# Nested: you have to keep every level in your head
if user is not None:
    if user_is_active:
        if has_permission:
            print("Access granted")
        else:
            print("No permission")
    else:
        print("Account disabled")
else:
    print("Not logged in")
```

Usually you can **flatten** it: handle each failure first and leave early, so the main path isn't indented at all. Inside a function, that looks like this (functions and `return` are the topic of "Functions"; `return` hands back a value and ends the function straight away):

```python
def check_access(user, user_is_active, has_permission):
    if user is None:
        return "Not logged in"
    if not user_is_active:
        return "Account disabled"
    if not has_permission:
        return "No permission"
    return "Access granted"
```

Each check is one line, in order, and the happy path is at the bottom. These early exits are called **guard clauses**. Professional code uses them everywhere.

## `match` (briefly)

When you're comparing one value against several fixed options, Python 3.10+ has `match`:

```python
command = "stop"
match command:
    case "start":
        print("Starting")
    case "stop" | "quit":
        print("Stopping")
    case _:
        print(f"Unknown command: {command}")
# Stopping
```

`|` means "or", and `case _:` catches everything else (like `else`). `match` can do much more (it can pull apart lists and dicts), but `if`/`elif` covers everything in this section. Use whichever reads more clearly.

## Edge cases: where bugs live

An **edge case** is an input at the boundary of what your code handles: the smallest and largest valid values, values just outside the range, zero, empty input. A program that works for "normal" input and breaks at the edges is the most common kind of bug.

Take a grading rule: 90 and above is an A, 80–89 is a B. The interesting inputs aren't 95 and 85; they're **89, 90, 80, 79, 100 and 0**, plus invalid ones like **101 and -1**. A test with 95 can't tell `score >= 90` from `score > 90`; a test with 90 can.

When the input itself is impossible (a score of 150), the function shouldn't silently guess an answer. Python's way to say "the caller gave me something invalid" is to **raise an error**:

```python
def check_score(score):
    if score < 0 or score > 100:
        raise ValueError(f"score must be between 0 and 100, got {score}")
    return score

check_score(150)
# ValueError: score must be between 0 and 100, got 150
```

`raise` stops the function immediately and reports the problem to whoever called it. You'll learn to raise and handle errors properly in the next section; for this lesson's exercises, this pattern is all you need.

Make a habit of it: before you write a condition, list its boundaries, and test each one.

## Common mistakes

**`=` instead of `==`.**

```python
if age = 18:
# SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**Forgetting the colon or the indentation.**

```python
if age >= 18
# SyntaxError: expected ':'

if age >= 18:
print("adult")
# IndentationError: expected an indented block after 'if' statement on line 1
```

**`or` that doesn't mean what English means.** `if colour == "red" or "blue":` is *always* true. Python reads it as `(colour == "red") or ("blue")`, and `"blue"` is a non-empty string, so it's truthy. Write `colour == "red" or colour == "blue"`, or `colour in ("red", "blue")`.

**Conditions in the wrong order.** Check the most specific case first: `FizzBuzz` (divisible by 3 *and* 5) must come before `Fizz`, and the 400-year rule comes before the 100-year rule in leap years.

**Using `if` where you meant `elif`.** A chain of separate `if`s checks every condition, so more than one block can run. `elif` stops at the first match.

**Treating 0 or `""` as "missing".** `if not value:` is also true for 0. Use `is None` when that matters.

## Recap

- Comparisons (`==`, `!=`, `<`, `<=`, `>`, `>=`) produce `True` or `False`. `=` assigns; `==` compares.
- `and`, `or` and `not` combine conditions. Use brackets when mixing them. They short-circuit.
- `if`/`elif`/`else` runs **only the first** matching block, so order matters. Indentation defines the block.
- Empty and zero values are **falsy**; almost everything else is **truthy**.
- Prefer flat code with **guard clauses** over deep nesting. `match` is a neat option for comparing one value against fixed choices.
- Bugs live at **edge cases**. Test the boundaries, and `raise ValueError` for impossible input.
