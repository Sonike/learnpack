# Tested library system

Add a proper safety net to the library system you built in the previous section's project. By the end, every rule is pinned down by tests, the tests run automatically on GitHub for every push, and you have practised the three habits that matter most on a team: test-first development, refactoring under test, and fixing bugs with a regression test.

Work in the same repository as your library system.

## 1. Set up pytest

Install `pytest` and `pytest-cov` in your project's virtual environment and add them to a `requirements-dev.txt` (or your `pyproject.toml`). Put tests in a `tests/` folder, one test file per module (`tests/test_fees.py`, `tests/test_library.py`, ...). Run them with:

```bash
pytest
```

## 2. Test every rule

Write unit tests for every rule in the library: loan limits, double-lending, returns, fees, the fee cap, the "owes too much" block and notifications. For each one, go through the edge-case checklist: empty, one, many, **boundaries** (exactly 3 loans, returned exactly on the due date, exactly 5.00 owed), and invalid input.

- Name each test after the behaviour: `test_member_with_three_loans_cannot_borrow`.
- Use table-driven tests (`pytest.mark.parametrize`) for the fee calculation.
- Test that rule-breaking raises the right exception, with `pytest.raises`.
- Test through public methods only, not private attributes.

## 3. Mocks only at the boundaries

The clock and the notifier are your boundaries. Use a fixed date (or a fake clock) and a `Mock` or your `InMemoryNotifier`. Everything else (books, members, loans, fee logic) should be real objects in your tests, not mocks.

## 4. Coverage

Measure branch coverage:

```bash
pytest --cov=library --cov-branch --cov-report=term-missing
```

Reach **90% or more**. Look at every line still listed under `Missing` and either test it or explain in the README why it doesn't need a test. Paste the coverage summary into the README.

## 5. Build one feature test-first

Add a new feature with TDD, for example **reservations**: a member can reserve a book that's on loan, the reserver is notified when it comes back, and nobody else can borrow it for 2 days. Commit at each step so the history shows the loop:

```bash
git log --oneline
```

```
a41c9e2 Refactor: extract Reservation dataclass
7d03b11 Green: notify the reserver when a book is returned
c9e1a50 Red: reserver is notified on return
...
```

## 6. Refactor under test

Pick the messiest function in your library (the longest, or the one with the deepest `if`s) and refactor it with your tests as the safety net: extract functions, replace a conditional with a lookup table, introduce a parameter object. Open a pull request for it that shows the before and after and states that no tests changed.

## 7. CI with GitHub Actions

Add `.github/workflows/tests.yml` that, on every push and pull request, installs your dependencies and runs `ruff check .`, then `pytest`. Add the workflow's status badge to the top of your README (GitHub shows the badge Markdown under the workflow's "..." menu: *Create status badge*).

## 8. A bug, reported and fixed properly

Find (or deliberately introduce, then forget about) a bug. Write it up as a GitHub issue: what you did, what you expected, what happened. Then fix it in a pull request whose first commit is a **failing regression test** and whose second commit is the fix. Link the pull request to the issue (`Fixes #12` in the description closes it on merge).

> **On AI tools:** an assistant is good at suggesting edge cases you missed. Ask it "what cases am I not testing?", but decide the expected values yourself from the rules, and never let it write both the code and the tests for the same feature.
