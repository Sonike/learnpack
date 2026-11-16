# Why and how we test

## Why this matters

Every time you change code, something that used to work might break. You could re-check everything by hand after every change, but you won't, and nobody on a team does. **Automated tests** are small programs that check your program for you, in seconds, every time. They're how professional teams change code confidently, how reviewers trust a pull request, and how you'll know whether a suggestion from an AI assistant actually works. Almost every software job expects you to write tests, and many interviews ask you to.

## A test is code that checks code

Here's a function:

```python
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

You could check it by printing results and eyeballing them:

```python
print(is_leap_year(2024))   # True
print(is_leap_year(1900))   # False
```

But then *you* are the test: you have to remember what the right answers are and read the output every time. Put the expected answer into the code instead, with `assert`:

```python
assert is_leap_year(2024) == True
assert is_leap_year(1900) == False
```

`assert condition` does nothing if the condition is true, and raises `AssertionError` if it's false:

```python
assert 1 + 1 == 2     # silent: fine
assert 1 + 1 == 3
# AssertionError
```

Silence means success; an error means something is wrong. That's the whole idea. Everything else in testing is about organising asserts well.

Add a message after a comma, so a failure explains itself:

```python
year = 1900
assert is_leap_year(year) == False, f"{year} is divisible by 100 but not 400, so not a leap year"
```

> **Note:** for `True`/`False` results you'll often see `assert is_leap_year(2024)` and `assert not is_leap_year(1900)`. Both styles work. Comparing with `==` can make failure messages clearer.

## Tests as executable specifications

Look at the asserts again. They're a precise description of what the function should do, written as examples:

```python
assert is_leap_year(2024)        # divisible by 4: leap
assert not is_leap_year(2023)    # not divisible by 4: not leap
assert not is_leap_year(1900)    # divisible by 100: not leap...
assert is_leap_year(2000)        # ...unless divisible by 400
```

That's a **specification** (a description of required behaviour) that a computer can check. Unlike a comment or a document, it can't silently go out of date: if the code stops matching it, the test fails. When you join a team, reading the tests is often the fastest way to learn what a piece of code is supposed to do.

## Test functions

Loose asserts at the bottom of a file get messy. Put them in **test functions**, each named for what it checks, with names starting `test_`:

```python
def test_ordinary_leap_year():
    assert is_leap_year(2024)


def test_century_is_not_a_leap_year():
    assert not is_leap_year(1900)


def test_every_400_years_is_a_leap_year():
    assert is_leap_year(2000)
```

The `test_` prefix matters: it's how test runners find your tests. A good name says what *behaviour* is being checked, so when one fails, the name alone tells you what broke.

## Arrange, act, assert

Most tests have the same three parts, and keeping them visible makes tests easy to read:

```python
def test_withdraw_reduces_balance():
    # Arrange: set up what the test needs
    account = BankAccount("Ada")
    account.deposit(100)

    # Act: do the one thing being tested
    account.withdraw(30)

    # Assert: check the result
    assert account.balance == 70
```

**Arrange-act-assert** (sometimes "given, when, then") is a habit worth building now. If the "act" part grows to several unrelated steps, you're probably testing more than one thing, and it should be two tests.

## Running tests with pytest

**pytest** is the standard test runner for Python. It finds files named `test_*.py`, runs every function named `test_*` in them, and reports the results. Put your code and tests in separate files:

```
leap/
├── leap.py          # is_leap_year lives here
└── test_leap.py     # from leap import is_leap_year, then the test functions
```

Install pytest in your project's virtual environment and run it from the project folder:

```bash
pip install pytest
pytest
```

```
============================= test session starts ==============================
collected 3 items

test_leap.py ...                                                         [100%]

============================== 3 passed in 0.01s ===============================
```

Each `.` is a passing test. `pytest -v` lists them by name instead.

## Reading a failure

Now break the function, say by forgetting the 400 rule, and run pytest again:

```bash
pytest
```

```
=================================== FAILURES ===================================
_____________________ test_every_400_years_is_a_leap_year ______________________

    def test_every_400_years_is_a_leap_year():
>       assert is_leap_year(2000)
E       assert False
E        +  where False = is_leap_year(2000)

test_leap.py:12: AssertionError
=========================== short test summary info ============================
FAILED test_leap.py::test_every_400_years_is_a_leap_year - assert False
========================= 1 failed, 2 passed in 0.02s ==========================
```

Read it from the top, the same way you read any error:

1. **Which test:** `test_every_400_years_is_a_leap_year`. A good name already tells you the 400 rule broke.
2. **Which line:** the `>` marks the assert that failed, and `test_leap.py:12` gives the line number.
3. **What happened:** the `E` lines. pytest rewrites asserts to show the values involved: `is_leap_year(2000)` returned `False`.
4. **The summary:** 1 failed, 2 passed.

For an `==` comparison, pytest shows both sides (`assert 'hello-world' == 'hello_world'`), and for lists and dicts it shows exactly which items differ. That's why plain `assert` with `==` is all you need with pytest.

> **Note:** the practice exercises on this platform run tests in exactly this style: plain `test_*` functions with `assert`. You can copy any exercise's code and tests into a folder and run `pytest` on your own machine.

## What a test can and can't prove

A passing test proves the code gives the right answer **for the inputs you tried**. That's all. It doesn't prove the code is correct for every input. If your tests only check 2024 and 2023, a function that ignores the century rules passes them perfectly.

So a test suite is only as good as the cases it covers. Ask yourself: if the code had a bug, would one of my tests fail? A good way to practise is to imagine specific bugs (forgot the 100 rule; got the 400 rule backwards; always returns `True`) and check that some test would catch each one. That's exactly what this lesson's exercise asks you to do. In the testing world, deliberately broken copies of code are called **mutants**, and checking that your tests catch them is **mutation testing**.

Tests also can't tell you whether you built the right thing. If you misunderstood the requirement, your code and your tests will agree with each other, and both will be wrong.

## Tests as a safety net

Tests pay off most when you change code:

- **Refactoring:** you restructure the code, run the tests, and know that behaviour is unchanged. Without tests, refactoring is guesswork (see the lesson "Code smells and refactoring").
- **Bug fixes:** you write a test that reproduces the bug, fix it, and the test stops the bug from ever quietly coming back.
- **Other people's changes:** tests run automatically on every pull request, so a teammate can't break your feature without finding out.
- **AI-generated code:** an assistant can produce plausible code that's wrong in an edge case. Your tests are how you find out before your users do. Writing the tests yourself, from the requirements, is also the best way to check that *you* understand what the code should do.

## Common mistakes

**A test that can't fail.** `assert is_leap_year(2024) or True` always passes. So does a test function that calls the code but never asserts anything. Make each new test fail once, on purpose (break the code or the expected value), to see it go red.

**Forgetting the `test_` prefix.** pytest silently skips `def check_leap_year():`. If pytest says `collected 0 items`, check your file and function names.

**Comparing floats with `==`.** `assert 0.1 + 0.2 == 0.3` fails: floats are approximate. Use `math.isclose(0.1 + 0.2, 0.3)` (or `pytest.approx`).

**Parentheses around assert.** `assert (x == 1, "message")` asserts a non-empty tuple, which is always true, so the test can never fail. Python even warns: `SyntaxWarning: assertion is always true, perhaps remove parentheses?`. Write `assert x == 1, "message"`.

**Testing everything in one function.** If `test_everything` fails, you don't know which of its twenty checks broke, and the ones after the failing assert never ran. One behaviour per test.

## Recap

- A test is code that checks code: call it, then `assert` the result.
- Tests are executable specifications: examples of required behaviour that can't go stale.
- Put asserts in `test_*` functions with descriptive names, arranged as arrange-act-assert.
- Run them with `pytest`; read failures top to bottom: test name, line, values.
- Tests prove behaviour only for the cases you wrote, so choose cases that would catch real bugs.
