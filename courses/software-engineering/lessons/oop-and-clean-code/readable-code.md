# Readable code

## Why this matters

Code is read far more often than it's written: by teammates reviewing your pull request, by whoever fixes a bug in it next year, and by you in three weeks when you've forgotten everything. On a real team, "it works" is the minimum. "Someone else can understand and change it safely" is the actual bar, and reviewers will hold you to it. The good news is that readable code isn't a talent. It's a handful of habits you can practise, and this lesson covers the ones that matter most.

## Names

A good name says what something *is* or *does*, so the reader doesn't have to work it out.

```python
# Before
def calc(d, r):
    t = 0
    for x in d:
        t += x["p"] * x["q"]
    return t * (1 - r)

# After
def order_total(items, discount_rate):
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]
    return subtotal * (1 - discount_rate)
```

Same logic. The second version needs no explanation. Some guidelines:

- **Variables are nouns** (`subtotal`, `user_email`); **functions are verbs** (`calculate_total`, `send_invoice`); **booleans read as yes/no questions** (`is_overdue`, `has_paid`, `can_edit`).
- **Say what's inside, including units when they matter**: `timeout_seconds`, `price_cents`, `weight_kg`. A bare `timeout = 30` has caused real outages when someone assumed milliseconds.
- **One-letter names are fine for tiny scopes** with a strong convention, like `i` in a short loop or `x, y` for coordinates. Not for anything that lives more than a few lines.
- **Avoid vague words**: `data`, `info`, `temp`, `handle`, `process`, `manager`, `stuff`. Everything is data. What kind?
- **Don't encode the type in the name** (`name_str`, `user_list`). Type hints do that job now; say what it means instead (`names`, `active_users`).

## Small functions that do one thing

A function should do one job you can describe in a short sentence without saying "and". `load_orders_and_email_report` is two functions trying to be one.

Small functions help in three ways. Their names act as headings, so the calling code reads like a summary. Each can be tested on its own. And bugs have fewer places to hide.

```python
def send_monthly_report(orders, mailer, now):
    recent = orders_in_month(orders, now)
    total = sum_totals(recent)
    body = format_report(recent, total)
    mailer.send("finance@example.com", body)
```

You can understand what this does in five seconds, and dive into whichever helper you care about. There's no magic number for length, but if you have to scroll, or you feel like adding a comment to label a section ("# now calculate the tax"), that section probably wants to be a function named after the comment.

## Guard clauses instead of deep nesting

Every level of indentation is something the reader has to keep in their head. Compare:

```python
def can_borrow(member, book):
    if member is not None:
        if member.is_active:
            if book.available:
                if len(member.loans) < 5:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
```

with:

```python
MAX_LOANS = 5

def can_borrow(member, book):
    if member is None or not member.is_active:
        return False
    if not book.available:
        return False
    return len(member.loans) < MAX_LOANS
```

The second uses **guard clauses**: check for the cases that end early, return right away, and let the main path run down the left edge with no nesting. When you see a pyramid of `if`s, flip the conditions and return early.

## Magic numbers

A **magic number** is a literal whose meaning isn't obvious: `if len(member.loans) < 5`, `price * 0.2`, `time.sleep(86400)`. Give it a name:

```python
MAX_LOANS = 5
VAT_RATE = 0.2
SECONDS_PER_DAY = 24 * 60 * 60
```

The name explains the number, and if the rule changes ("members can now borrow 8 books"), you change it in one place. By convention, constants are `UPPER_CASE` at the top of the module. `0`, `1` and `100` for percentages are usually fine as they are.

## Comments that explain *why*

Code already says *what* it does. A comment that repeats it is noise, and it goes stale the moment someone edits the code but not the comment:

```python
# Bad: says what the code already says
i += 1  # add one to i

# Good: says why, which the code can't
# The payments API counts days from 1, not 0.
day_index += 1
```

Good comments explain reasons, warnings and context: why this odd approach, which bug a line works around, what a reader must not change. If you need a comment to explain *what* a block does, try renaming or extracting a function first.

A **docstring** is different: a string right under a `def` or `class` line that tells the *caller* how to use it. Write one for anything other people will call:

```python
def split_bill(total_cents: int, people: int) -> list[int]:
    """Split a bill into shares that add up to total_cents exactly.

    Leftover cents go one each to the first people.
    """
```

## Separating logic from input and output

This is the design habit with the biggest payoff. Look at this function:

```python
def report():
    name = input("Name? ")
    with open("scores.txt") as f:
        scores = [int(line) for line in f]
    average = sum(scores) / len(scores)
    print(f"{name}: average {average:.1f}")
```

It reads from the keyboard, reads a file, calculates and prints, all tangled together. To test whether the average is right, you'd need a keyboard, a file and a way to capture the screen. Now split it:

```python
def average(scores: list[int]) -> float:
    return sum(scores) / len(scores)


def format_line(name: str, avg: float) -> str:
    return f"{name}: average {avg:.1f}"


def report() -> None:
    name = input("Name? ")
    with open("scores.txt") as f:
        scores = [int(line) for line in f]
    print(format_line(name, average(scores)))


print(format_line("Ada", average([90, 85, 77])))   # Ada: average 84.0
```

`average` and `format_line` are **pure functions**: their result depends only on their arguments, and they have no **side effects** (no printing, no file or network access, no changing anything outside themselves). Pure functions are trivial to test (call, compare), easy to reuse and easy to reason about. The I/O (input and output) is pushed out to a thin outer layer, `report`, which has almost nothing left in it to go wrong.

The pattern to aim for: **a pure core with a thin I/O shell.** You'll use it in every project from here on, and it's the main thing that makes the next section of the course, on testing, go smoothly.

## Style, formatters and linters

**PEP 8** is Python's official style guide: four-space indents, `snake_case` functions, `PascalCase` classes, `UPPER_CASE` constants, spaces around operators, two blank lines between top-level functions. You don't need to memorise it, because tools apply it for you:

- A **formatter** rewrites your code's layout automatically, so nobody argues about spacing in reviews.
- A **linter** reads your code and warns about likely bugs and bad habits: unused imports, unused variables, a bare `except:`, `== None` instead of `is None`.

**Ruff** does both, very fast, and is now the default choice in most new Python projects:

```bash
pip install ruff
ruff format .
ruff check .
```

`ruff format .` might print `2 files reformatted, 5 files left unchanged`. `ruff check .` prints one line per problem, then a summary:

```
report.py:1:8: F401 [*] `os` imported but unused
Found 1 error.
[*] 1 fixable with the `--fix` option.
```

Each line is file, line, column, a rule code (look it up in the ruff docs if it's unfamiliar) and the message. `ruff check --fix .` fixes the safe ones for you. Most teams run both in CI so style never comes up in code review.

> **Try it:** in the Python REPL, run `import this`. It prints "The Zen of Python" (PEP 20), a short list of the values behind Python's design. "Readability counts" is one of them.

## Duplication is cheaper than the wrong abstraction

You'll hear "DRY: don't repeat yourself". It's good advice with a trap in it. When two pieces of code look alike, it's tempting to merge them into one function straight away. But if they only *look* alike and change for different reasons, the shared function soon grows flags and special cases (`def save(item, is_invoice=False, skip_tax=False, legacy_mode=False)`) until nobody can change it safely.

A practical rule: **wait for the third copy.** Two similar blocks can stay duplicated. When a third appears and you can now see what genuinely stays the same, extract it. And if a shared function has grown a tangle of flags, it's fine to copy it back into its callers and simplify each one.

## Common mistakes

**Renaming without updating every use.** You get `NameError: name 'calc' is not defined`. Use your editor's "Rename symbol" (F2 in VS Code) instead of find-and-replace by hand.

**Refactoring and changing behaviour in the same step.** If the output changes, you can't tell whether the cleanup or the "small improvement" caused it. Clean first, check that nothing changed, then change behaviour.

**Comments that lie.** An out-of-date comment is worse than none. When you change code, read the comments around it.

**Printing inside helpers.** A helper that prints can't be reused anywhere the output should go somewhere else (a file, a web page, a test). Return a string; let the outer layer print it.

**Clever one-liners.** A triple-nested list comprehension might be short, but if a reader has to stop and decode it, a plain loop is better.

## Recap

- Names say what things are and do, with units where they matter. Booleans read as questions.
- Small functions with one job; guard clauses instead of nested `if`s; named constants instead of magic numbers.
- Comments explain *why*; docstrings tell callers how to use a function.
- Keep logic pure and push input and output to a thin outer layer. It's what makes code testable.
- Let ruff handle style. Wait for the third copy before abstracting.
