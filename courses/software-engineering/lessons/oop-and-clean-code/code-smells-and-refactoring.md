# Code smells and refactoring

## Why this matters

Your first job will almost certainly not be writing new code from scratch. It will be changing code that already exists, often code that's grown messy over years. Knowing how to spot what's wrong with it (**code smells**) and how to improve it in small, safe steps (**refactoring**) is one of the most practical skills a junior engineer can have. It's also what interviewers mean when they ask "how would you improve this?"

## What refactoring is (and isn't)

**Refactoring** means changing the structure of code **without changing what it does**. Renaming a variable, splitting a long function, replacing a chain of `if`s with a dictionary: all refactoring. Adding a feature or fixing a bug is not refactoring; it's a behaviour change.

The two kinds of change should happen at separate times. Kent Beck's version of this: "make the change easy, then make the easy change." First refactor until the new feature has an obvious place to go, while the behaviour stays the same. Then add the feature.

How do you know the behaviour stayed the same? **Tests.** Before refactoring, you need tests that pin down what the code does now. If the code has none, write some first. Tests that record current behaviour, whether it's "right" or not, are called **characterization tests**:

```python
# Characterization tests for a legacy function: record what it does TODAY.
assert legacy_price("book", 2) == 1800
assert legacy_price("book", 0) == 0
assert legacy_price("ebook", 1) == 500
```

Run them after every small step. If one fails, undo the last step. It was small, so you've lost almost nothing.

## Code smells

A **code smell** is a surface sign that often points to a deeper problem. A smell isn't automatically a bug, and not every smell needs fixing; it's a prompt to look closer. The names come from Martin Fowler and Kent Beck's book *Refactoring*, and they're used across the industry, so learning them gives you a shared vocabulary for code review.

**Long function.** A function you have to scroll through, with comments labelling its sections. It's hard to understand, test or reuse. Fix: **extract function** for each section.

**Duplicated code.** The same few lines in several places. Fix a bug in one and you've left it in the others. Fix: extract the common part (once you've seen it three times; see "Duplication is cheaper than the wrong abstraction" in the lesson "Readable code").

**Long parameter list.**

```python
def create_booking(name, email, phone, start_day, start_month, start_year,
                   end_day, end_month, end_year, room, guests):
    ...
```

Easy to pass arguments in the wrong order, and every caller has to change when one is added. Fix: **introduce parameter object**: group the values that travel together into a dataclass, such as `Guest(name, email, phone)` and `DateRange(start, end)`.

**Feature envy.** A function that's more interested in another object's data than its own:

```python
def shipping_label(order):
    c = order.customer
    return f"{c.name}\n{c.street}\n{c.city} {c.postcode}"
```

Every line reaches into `customer`. Fix: **move function** onto the class whose data it uses, as `customer.mailing_address()`.

**Primitive obsession.** Using raw strings, ints and dicts for ideas that deserve their own type: a price as a float, a status as a free-text string, an email as a bare `str` that's validated in twelve places. Fix: small types, such as a `Money` dataclass, a `Status` enum or an `Email` class that validates once on creation.

**Long `if/elif` chains on a type or kind.**

```python
def shipping_cost(zone, kg):
    if zone == "local":
        return 300 + 50 * kg
    elif zone == "national":
        return 600 + 100 * kg
    elif zone == "europe":
        return 1300 + 250 * kg
    # ... and four more
```

Each branch does the same calculation with different numbers. Adding a zone means copying a branch. Fix below.

## The core refactoring moves

You can go a long way with four moves.

**1. Rename.** The cheapest, highest-value refactoring. Use your editor's "Rename symbol" so every use updates at once.

**2. Extract function.** Pull a section out into a named function:

```python
# Before
def print_invoice(order):
    total = 0
    for line in order.lines:
        total += line.price * line.qty
    if order.customer.is_member:
        total = total * 90 // 100
    print(f"Invoice for {order.customer.name}: {total}")

# After
MEMBER_DISCOUNT_PERCENT = 10

def invoice_total(order):
    total = sum(line.price * line.qty for line in order.lines)
    if order.customer.is_member:
        total -= total * MEMBER_DISCOUNT_PERCENT // 100
    return total

def print_invoice(order):
    print(f"Invoice for {order.customer.name}: {invoice_total(order)}")
```

Now `invoice_total` is pure and testable on its own, and `print_invoice` is one line.

**3. Introduce parameter object.** Shown above: `create_booking(guest, dates, room, guests)` instead of eleven loose arguments.

**4. Replace conditional with a lookup table (or polymorphism).** When the branches differ only in *data*, move the data into a dict:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Rate:
    base_cents: int
    per_kg_cents: int


RATES = {
    "local": Rate(300, 50),
    "national": Rate(600, 100),
    "europe": Rate(1300, 250),
}


def shipping_cost(zone: str, kg: int) -> int:
    if zone not in RATES:
        raise ValueError(f"unknown zone: {zone}")
    rate = RATES[zone]
    return rate.base_cents + rate.per_kg_cents * kg


print(shipping_cost("europe", 2))   # 1800
```

Adding a zone is now one line of data with no new logic. The rates could even move to a config file later. When the branches differ in *behaviour*, not just numbers, the equivalent move is **polymorphism**: give each kind its own class with the same method (as in the lesson "Inheritance, composition and interfaces"), or map each kind to a function in a dict.

> **Try it:** take any `if/elif` chain you wrote in an earlier section and ask: do the branches differ only in values? If so, rewrite it as a dict lookup.

## Refactoring safely, step by step

Here's the routine, whatever the move:

1. Make sure tests cover the code you're about to change. If not, write characterization tests.
2. Run them: all green.
3. Make **one** small change.
4. Run the tests again. Green? Commit. Red? Undo and take a smaller step.
5. Repeat.

Committing after each green step (`git commit -m "Extract invoice_total"`) means you can always get back to working code. It also makes your pull request easy to review: a reviewer can follow each step instead of facing one giant diff.

This is also the safe way to use AI tools on messy code. An assistant can suggest a refactoring and explain the smell, but the tests are what tell you its suggestion didn't change behaviour. Never accept a large AI-written "cleanup" of code that has no tests.

## Technical debt

**Technical debt** is Ward Cunningham's metaphor for the cost of shortcuts. Shipping a quick, messy solution is like borrowing money: you get something now, and you pay "interest" later, as every future change to that code is slower and riskier. Paying down the debt means refactoring.

Debt isn't always bad. Taking a shortcut to hit a launch date can be the right business call, as long as it's a *choice*, and it's paid back before the interest piles up. Fowler's "technical debt quadrant" separates prudent, deliberate debt ("we'll ship now and clean up next sprint") from reckless debt ("what's a function?"). As a junior, the useful habits are:

- Leave code a bit better than you found it: rename one confusing variable, extract one function, in the area you're already working in.
- When you take a deliberate shortcut, say so in the pull request or a ticket, so it's tracked rather than forgotten.
- Don't start a big rewrite of code you don't understand yet. Read it, test it, then improve it in small steps.

## Common mistakes

**Refactoring without tests.** You'll change behaviour without noticing. Characterization tests first, always.

**Mixing refactoring with feature work in one commit.** If something breaks, you can't tell which part broke it, and the reviewer can't either.

**Big-bang rewrites.** "I'll just rewrite the whole module" usually ends with a new module that has new bugs and lost some old, important edge-case handling nobody wrote down. Small steps keep you shipping.

**Treating every smell as a must-fix.** A long function that nobody has touched in three years and that has no bugs may be fine where it is. Refactor what you need to change.

**Over-abstracting the fix.** Replacing a three-branch `if` with an abstract base class, a factory and a plugin registry isn't an improvement. Choose the simplest structure that removes the smell.

## Recap

- Refactoring changes structure, not behaviour. Do it in small steps, with tests run after each one.
- No tests? Write characterization tests that record what the code does today.
- Learn the smells by name: long function, duplicated code, long parameter list, feature envy, primitive obsession, long conditionals.
- The core moves: rename, extract function, introduce parameter object, replace conditional with a lookup table or polymorphism.
- Technical debt is a trade-off. Take it on deliberately, record it, and pay it down where you're working.
