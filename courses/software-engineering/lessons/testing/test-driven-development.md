# Test-driven development

## Why this matters

Most beginners write code first and tests afterwards, if at all. **Test-driven development (TDD)** flips the order: you write a failing test, then just enough code to pass it, then tidy up, in short loops of a few minutes each. It sounds slow. In practice it keeps you out of the long debugging sessions that come from writing a hundred lines and then finding out they don't work. Even teams that don't use TDD for everything use its most valuable habit daily: **when you fix a bug, write the test that reproduces it first.**

## Red, green, refactor

TDD is a loop of three steps:

```
      ┌──────────────────────────────────────────────┐
      │                                              │
      ▼                                              │
   1. RED            2. GREEN             3. REFACTOR
   Write a test      Write the least      Clean up the code
   for the next      code that makes      (and the tests),
   small piece of    it pass. Ugly is     keeping every test
   behaviour.        fine.                green.
   Watch it FAIL.
```

1. **Red.** Write one test for the next small piece of behaviour. Run it and watch it **fail**. This step proves the test can fail, so it's actually testing something.
2. **Green.** Write the *simplest* code that makes it pass. Not the general solution, not the clever one: the least you can get away with.
3. **Refactor.** Now that everything passes, improve the code: better names, removing duplication, extracting functions. Run the tests after each change; they must stay green.

Then pick the next small piece of behaviour and go round again.

## A worked example: the string calculator

Let's build `add(numbers: str) -> int`, which sums the numbers in a string like `"1,2,3"`. We'll do it TDD style, the same kata you'll do in the practice exercise.

**Round 1, red.** The simplest behaviour: an empty string gives 0.

```python
def test_empty_string_is_zero():
    assert add("") == 0
```

Run it. It fails with `NameError: name 'add' is not defined`. Red, as expected.

**Green.** The least code that passes:

```python
def add(numbers: str) -> int:
    return 0
```

Yes, really. It passes. This looks silly, but it's a real discipline: every line you write is there because a test demanded it.

**Round 2, red.** One number returns itself.

```python
def test_single_number():
    assert add("4") == 4
```

Fails: `assert 0 == 4`. **Green:**

```python
def add(numbers: str) -> int:
    if numbers == "":
        return 0
    return int(numbers)
```

Both tests pass.

**Round 3, red.** Two numbers separated by a comma.

```python
def test_two_numbers():
    assert add("1,2") == 3
```

Fails: `ValueError: invalid literal for int() with base 10: '1,2'`. **Green:**

```python
def add(numbers: str) -> int:
    if numbers == "":
        return 0
    return sum(int(part) for part in numbers.split(","))
```

All three pass.

**Refactor.** Is there anything to clean up? `if numbers == ""` could be `if not numbers`. Make the change, run the tests: still green. Notice we never wrote a special case for "exactly two numbers": the general version fell out naturally, and it already handles `"1,2,3,4"` too.

Each loop took a minute or two, and at every moment we had working code and a test proving it.

> **Try it:** continue the kata yourself in the practice exercise: newlines as separators, custom delimiters, then negative numbers. Resist reading ahead.

## Taking the smallest step

The skill in TDD is choosing small steps. If you write a test and then need twenty minutes and fifty lines to make it pass, the step was too big. Back out and write a smaller test.

Small steps have a big payoff: when a test fails, the bug is almost certainly in the few lines you just wrote. You rarely need a debugger.

**Triangulation** is a technique for when you're not sure how to generalise. Write a second example that forces the general code. One test, `add("4") == 4`, can be passed by `return 4`. A second test, `add("7") == 7`, rules out the hard-coded answer and forces `return int(numbers)`. Two examples pointing the same way "triangulate" the real rule.

## When a test passes immediately

Sometimes you write a new test, run it, and it's green straight away. Don't celebrate yet. Something's off, and it's one of these:

- **The behaviour already exists.** Your earlier code was more general than you thought (like the "many numbers" case above). That's fine, and the test still has value as documentation, but confirm it by temporarily breaking the code and checking that the test goes red.
- **The test is broken.** It's not testing what you think: it calls the wrong function, the assert can never fail, or pytest isn't even running it (a missing `test_` prefix).

The rule: **never trust a test you haven't seen fail.**

## Fixing bugs test-first

This is the part of TDD everyone should use, all the time. A bug report comes in:

> Splitting a 10.00 bill between 3 people charges 3.33 each, which only adds up to 9.99.

Here's the code:

```python
def split_bill(total_cents: int, people: int) -> list[int]:
    share = total_cents // people
    return [share] * people


print(split_bill(1000, 3))   # [333, 333, 333]
```

Before touching the code, **write a test that reproduces the bug**:

```python
def test_shares_add_up_to_the_total():
    shares = split_bill(1000, 3)
    assert sum(shares) == 1000, f"{shares} adds up to {sum(shares)}, not 1000"
```

Run it: red, `AssertionError: [333, 333, 333] adds up to 999, not 1000`. Good: now you've proven you understand the bug and can reproduce it on demand. Fix the code:

```python
def split_bill(total_cents: int, people: int) -> list[int]:
    share, leftover = divmod(total_cents, people)
    return [share + 1 if i < leftover else share for i in range(people)]


print(split_bill(1000, 3))   # [334, 333, 333]
```

`divmod(1000, 3)` returns both the whole-number division and the remainder: `(333, 1)`. The one leftover cent goes to the first person. Run the test: green. Keep it forever. A test written to stop a fixed bug from coming back is called a **regression test** (a "regression" is when something that worked breaks again).

Why test first and not after? If you fix first and then write the test, you never see the test fail on the buggy code, so you don't know it would have caught the bug. A good bug-fix pull request contains the test and the fix together, and reviewers often check out the test alone to watch it fail.

## When TDD helps and when it doesn't

TDD shines when:

- **The rules are clear** and can be written as examples: parsing, calculations, validation, business rules (late fees, discounts, permissions).
- **You're fixing a bug.** Always reproduce it with a test first.
- **The code is tricky** and you'd otherwise be tempted to write a lot of it at once.
- **You're designing an interface.** Writing the test first makes you use the function before it exists, which quickly shows whether its name and parameters are awkward.

It helps less when:

- **You're exploring.** If you don't know yet what you're building (trying out a new library, sketching a UI, checking whether an idea is even possible), write a quick throwaway **spike** with no tests. Once you know what you want, delete the spike and build it properly, test-first if you like.
- **The output is judged by eye**, like the exact layout of a page.

TDD is a tool, not a religion. Plenty of excellent engineers write tests just after the code, in small steps. What matters is that the tests exist, that you've seen them fail, and that you never write large amounts of untested code.

> **Note:** TDD pairs well with AI assistants. You write the test, which pins down exactly what you want, in your own words. If you then ask an assistant for help, the test tells you immediately whether its suggestion works. Writing the tests yourself also keeps *you* in charge of what the code should do.

## Common mistakes

**Skipping the red step.** Writing a test and code together, then running both, means you've never seen the test fail. It might not test anything.

**Writing too much code in the green step.** "While I'm here I'll also handle negatives" means untested code. Write a test for negatives first.

**Skipping the refactor step.** Green isn't done. The deliberately simple code from each green step piles up into a mess if you never tidy it.

**Refactoring while red.** Only restructure when everything passes. Otherwise you can't tell whether a failure is the new feature or your cleanup.

**Steps that are too big.** If you've been red for more than ten minutes, undo back to green and write a smaller test.

## Recap

- TDD is a loop: **red** (write a failing test), **green** (the least code to pass), **refactor** (clean up while green).
- Take the smallest step that moves you forward; use triangulation to force the general solution.
- A test that passes immediately needs checking: break the code and confirm it goes red.
- Fix every bug test-first: reproduce it with a regression test, watch it fail, then fix it.
- Use TDD where rules are clear; spike freely when exploring, then rebuild with tests.
