# Fix a bug test-first

A bug report has come in:

> **Bill split loses money.** Splitting a 10.00 bill between 3 people charges 3.33 each, which only adds up to 9.99. The restaurant is a cent short on every bill like this.

Here is the function the report is about (it's also in the starter):

```python
def split_bill(total_cents: int, people: int) -> list[int]:
    share = total_cents // people
    return [share] * people
```

Fix it the test-first way, in two parts.

**Part 1: the regression test.** Write `check_regression(fn)` that **fails** (raises `AssertionError`) on the buggy version above and passes on a correct one. A **regression test** reproduces a bug so it can never quietly come back. Run it against the buggy version *before* you fix anything and make sure it fails: a regression test that has never failed hasn't proven anything.

**Part 2: the fix.** Change `split_bill` so the shares always add up to exactly `total_cents`:

- Everyone gets `total_cents // people` cents, and the leftover cents (`total_cents % people`) go **one each to the first people** in the list. So `split_bill(1000, 3)` is `[334, 333, 333]` and `split_bill(1001, 3)` is `[334, 334, 333]`.
- `people` must be at least 1; otherwise raise `ValueError`.

```python
def check_regression(fn) -> None: ...
def split_bill(total_cents: int, people: int) -> list[int]: ...
```

The hidden tests run your checker on the buggy version (must fail), on a correct version (must pass) and on a wrong "fix" that rounds everyone up to 334 (must fail: the total is 10.02 now, which is a new bug). Then they test your `split_bill`.

> **Tip:** the strongest assert here isn't about any one share. It's `sum(fn(total, people)) == total` for a few totals that don't divide evenly.
