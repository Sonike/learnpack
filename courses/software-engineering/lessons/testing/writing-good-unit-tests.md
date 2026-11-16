# Writing good unit tests

## Why this matters

Bad tests are worse than they look. A test suite that misses bugs gives false confidence; a test suite that breaks every time you tidy the code makes people stop running it. Good tests catch real bugs, fail with a message that points straight at the problem, and keep passing when you restructure code without changing what it does. This lesson is about writing that kind of test, and about the skill at its centre: thinking of the cases most likely to break.

## What a unit test is

A **unit test** checks one small piece of code (a "unit": usually one function or one class) on its own, with no database, network or files involved. Unit tests are fast (thousands run in seconds), and when one fails it points at one small piece of code. Most of your tests will be unit tests. The lesson "Testing strategy" covers the other kinds.

## One behaviour per test

Each test should check one behaviour, and its name should say which:

```python
# One test checking everything
def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("Café") == "cafe"
    assert slugify("a -- b") == "a-b"
    assert slugify("") == ""
```

If this fails, the name tells you nothing, and the asserts after the failing one never run, so you don't know whether one rule broke or four. Compare:

```python
def test_spaces_become_dashes():
    assert slugify("Hello World") == "hello-world"


def test_accents_become_plain_letters():
    assert slugify("Café") == "cafe"


def test_runs_of_separators_become_one_dash():
    assert slugify("a -- b") == "a-b"


def test_empty_title_gives_empty_slug():
    assert slugify("") == ""
```

Now a failure reads like a bug report: `FAILED test_accents_become_plain_letters`. Name tests after the behaviour, in plain words: `test_rejects_negative_age`, `test_overdue_tasks_get_one_reminder`. Not `test_1` or `test_slugify_works`.

"One behaviour" doesn't always mean one assert. Checking both the returned value and the saved state of one action is fine; checking three unrelated rules is not.

## Edge cases: where the bugs live

Most bugs hide at the edges, not in the ordinary middle. When you test a function, walk through this checklist:

| Kind | Ask | For a function that sums a list |
|---|---|---|
| **Empty** | nothing at all? | `[]` |
| **One** | a single item? | `[5]` |
| **Many** | several, including repeats? | `[1, 2, 2, 3]` |
| **Boundaries** | exactly at a limit, and one either side? | the maximum size; `0`; `-1` |
| **Invalid** | wrong type, wrong format, out of range? | `None`, `["a"]` |
| **Special values** | zero, negatives, unicode, whitespace? | `[-3, 3]`, `[0]` |

**Boundaries** deserve extra attention. If a library allows 5 loans, test 4, 5 and 6 loans. Off-by-one mistakes (`<` where you meant `<=`) are among the most common bugs in all of programming, and only a test exactly at the boundary catches them.

For text, add: empty string, only spaces, leading and trailing spaces, repeated separators, capital letters, accents and other non-ASCII characters, and punctuation.

> **Try it:** pick any function you wrote in an earlier section and list one input for each row of the table. How many of them did you actually test?

## Table-driven tests

When you have many input/output pairs for the same behaviour, writing a function for each is repetitive. Put the cases in a list and loop:

```python
CASES = [
    ("Hello World", "hello-world"),
    ("Café au lait", "cafe-au-lait"),
    ("  padded  ", "padded"),
    ("a -- b", "a-b"),
]


def test_slugify_table():
    for title, want in CASES:
        got = slugify(title)
        assert got == want, f"slugify({title!r}): expected {want!r}, got {got!r}"
```

The message includes the input, so a failure says exactly which row broke. Adding a case is one line, which makes you more likely to add them.

pytest has a built-in way to do this that reports each row as a separate test:

```python
import pytest


@pytest.mark.parametrize("title, want", [
    ("Hello World", "hello-world"),
    ("Top 10 Tips", "top-10-tips"),
    ("a -- b", "a-b"),
])
def test_slugify(title, want):
    assert slugify(title) == want
```

```
test_slug.py::test_slugify[Hello World-hello-world] PASSED
test_slug.py::test_slugify[Top 10 Tips-top-10-tips] PASSED
test_slug.py::test_slugify[a -- b-a-b] PASSED
```

Same idea, nicer report. The practice exercises here use the loop version, since they run without pytest, but in your own projects `parametrize` is the norm.

## Testing exceptions

When the right behaviour is an error, test that the error happens. Without pytest:

```python
def test_rejects_negative_withdrawal():
    account = BankAccount("Ada")
    try:
        account.withdraw(-5)
    except ValueError:
        return                      # the error we wanted: pass
    raise AssertionError("withdraw(-5) should raise ValueError")
```

The final line matters. Without it, the test passes even if no error is raised. With pytest, use `pytest.raises`, which does the same thing more neatly:

```python
import pytest


def test_rejects_negative_withdrawal():
    account = BankAccount("Ada")
    with pytest.raises(ValueError, match="positive"):
        account.withdraw(-5)
```

The test passes only if the block raises `ValueError` with a message containing "positive". Be specific about the exception type. `pytest.raises(Exception)` also passes when the code crashes with a `TypeError` from a typo, which is exactly the kind of bug you want to catch.

## Test behaviour, not implementation

A good test checks *what* code does (its inputs and outputs, its visible effects), not *how* it does it. Compare two tests for a `TaskList`:

```python
# Tests implementation: reaches into private data
def test_add_task():
    tasks = TaskList()
    tasks.add("Buy milk")
    assert tasks._tasks == {1: Task(1, "Buy milk")}


# Tests behaviour: uses only the public methods
def test_added_task_is_listed_as_todo():
    tasks = TaskList()
    tasks.add("Buy milk")
    assert [t.title for t in tasks.by_status(Status.TODO)] == ["Buy milk"]
```

The first test breaks if you switch the internal dict to a list, even though everything still works for every user of the class. Tests like that make refactoring painful: you change nothing visible and twenty tests go red. The second test only breaks if the behaviour actually breaks.

Warning signs that a test is checking implementation details:

- It reads or sets attributes starting with `_`.
- It asserts *how many times* an internal helper was called, or in what order.
- It breaks when you rename a private function or reorganise code without changing any output.

## Readable tests

Tests are code that people read, often when something's on fire. Make them easy:

- **Obvious values.** `deposit(100); withdraw(30); assert balance == 70` beats `deposit(8371); withdraw(2914); assert balance == 5457`.
- **No logic in tests.** If a test has `if` statements or recalculates the expected answer with the same formula as the code, a bug in the formula will be in both places. Write the expected value literally.
- **Small helpers for repeated setup** are fine (`def make_account(balance): ...`), as long as each test still reads clearly on its own.
- **Some duplication is okay in tests.** Clarity beats cleverness here even more than in production code.

## Common mistakes

**No edge cases.** Only testing the happy path ("Hello World") misses most bugs. Use the checklist.

**The missing raise.** A `try/except` test without the final `raise AssertionError(...)` passes even when no exception happens.

**Over-broad exception checks.** `except Exception:` in a test hides typos in your code as "expected errors".

**Tests that depend on each other.** If `test_b` only passes when `test_a` ran first (say they share a module-level list), the suite breaks when run in a different order or one at a time. Each test should build everything it needs.

**Copying the answer from the code.** Running the function, pasting its output into the assert, and calling it a test only records what the code does, not what it *should* do. Work out the expected answer from the requirements.

**Letting an AI write tests for code it also wrote.** The tests will tend to share the code's misunderstandings. Use AI to suggest edge cases you missed, then decide the expected values yourself.

## Recap

- A unit test checks one small unit, fast and in isolation. One behaviour per test, named in plain words.
- Edge cases (empty, one, many, boundaries, invalid, special values) are where bugs live.
- Table-driven tests (a loop, or `pytest.mark.parametrize`) make many cases cheap.
- Test exceptions explicitly, with the specific type.
- Test behaviour through the public interface, not private details, so refactoring doesn't break tests.
