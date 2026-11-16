# Testing strategy

## Why this matters

You now know how to write unit tests and how to replace dependencies with doubles. But a suite made only of unit tests with fakes can pass while the real application is broken: the SQL has a typo, or two pieces that each work fine don't fit together. A suite made only of slow, whole-app tests takes an hour to run and nobody runs it. A **testing strategy** is the deliberate mix of test types that gives you confidence quickly. It's also a common interview question: "how would you test this?"

## Three kinds of test

**Unit tests** check one function or class on its own, with doubles for anything external. Milliseconds each. When one fails, it points at a few lines of code.

**Integration tests** check that several real pieces work together: your repository class with a real database, your API route with your real service layer. Slower (milliseconds to seconds) and they cover the "glue" that unit tests fake out.

**End-to-end (e2e) tests** drive the whole system the way a user would: start the app, send real HTTP requests or click through a real browser, check what comes back. They give the most realistic confidence, but they're the slowest, the hardest to set up and the most likely to be flaky, and when one fails it could be anything.

Some examples, for an app that stores tasks:

| Test | Kind |
|---|---|
| `is_overdue(task, now)` returns `True` for yesterday's date | unit |
| `send_reminders` with a mock mailer calls `send` once | unit |
| `TaskRepository.add` then `get` against a real SQLite database | integration |
| `POST /tasks` through the web framework's test client stores a row in SQLite | integration |
| A script starts the deployed app, signs up, creates a task and sees it listed | end-to-end |
| A browser automation tool clicks "Add task" and checks the page | end-to-end |

## The test pyramid

The classic guide for the mix is the **test pyramid**:

```
            /\
           /  \        a few end-to-end tests
          / E2E\       (slow, realistic, brittle)
         /------\
        /        \     some integration tests
       /integration\   (real database, real wiring)
      /------------\
     /              \  many unit tests
    /      unit      \ (fast, precise, cheap)
   /__________________\
```

Write **lots** of unit tests, because they're cheap and precise. Write **some** integration tests for the places where your code meets the outside world: the database, the web framework, files. Write **a few** end-to-end tests for the handful of journeys that must never break (sign up, log in, pay).

The opposite shape, mostly e2e tests and few unit tests, is sometimes called the "ice-cream cone", and it's what teams end up with when they bolt tests on at the end. The suite is slow and flaky, and every failure needs an investigation.

The pyramid is a guide, not a law. A small app that's mostly database queries might sensibly have more integration tests than unit tests. The principle underneath is what matters: **push each test as far down the pyramid as it can go while still catching the bug you care about.**

## Integration tests with a real SQLite database

Unit tests with a fake repository can't tell you whether your SQL is right. For that you need the real database. SQLite makes this easy: `sqlite3.connect(":memory:")` creates a complete, real SQL database that lives only in memory, takes about a millisecond to create, and disappears when the connection closes.

```python
import sqlite3


class TaskRepository:
    def __init__(self, conn):
        self.conn = conn
        conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")

    def add(self, title):
        return self.conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,)).lastrowid

    def complete(self, task_id):
        return self.conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)).rowcount == 1

    def is_done(self, task_id):
        row = self.conn.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return bool(row[0])


def make_repo():
    return TaskRepository(sqlite3.connect(":memory:"))


def test_complete_only_marks_that_task():
    repo = make_repo()
    first = repo.add("first")
    second = repo.add("second")

    repo.complete(first)

    assert repo.is_done(first) is True
    assert repo.is_done(second) is False
```

A few habits that make integration tests reliable:

- **A fresh database per test.** `make_repo()` creates a new in-memory database every time, so tests can't leak data into each other and can run in any order.
- **Test with more than one row.** The test above adds two tasks for a reason: if someone forgets the `WHERE` clause in `complete`, every task gets marked done, and only a test with a second task notices.
- **Test the "not found" paths.** What does `complete(999)` return? What does `get(999)` do? Those are where repository bugs hide.

> **Note:** if production uses PostgreSQL or another database, SQLite in memory is a fast stand-in for most queries, but not all SQL behaves identically. Teams that rely on database-specific features run some integration tests against the real database engine too, often in a throwaway container. You'll meet databases properly in the "Databases and SQL" section.

## Coverage: a flashlight, not a target

**Code coverage** measures which lines of your code ran during the tests. With pytest, the `pytest-cov` plugin reports it:

```bash
pip install pytest-cov
pytest --cov=tasks --cov-branch --cov-report=term-missing
```

```
Name       Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------
tasks.py      40      3     12      2    90%   31-33, 45->47
------------------------------------------------------
TOTAL         40      3     12      2    90%
```

`Missing` lists line numbers that never ran: lines 31–33, and a branch from line 45 to 47 that was never taken. `--cov-branch` adds **branch coverage**, which checks that both sides of every `if` ran, not just the line itself. That's much more useful than line coverage alone.

Use coverage as a **flashlight**: it shows you code that no test even touches, which is worth a look. Don't use it as a **target**. 100% coverage does not mean the code is correct or well tested:

```python
def average(scores):
    return sum(scores) / len(scores)


def test_average():
    average([1, 2, 3])        # no assert at all!
```

That's 100% coverage, and the test checks nothing. Coverage also can't see missing code: if you forgot to handle an empty list, there's no line for coverage to report as untested. When a team makes coverage a hard target, people write tests to hit lines rather than to catch bugs. A sensible stance: look at what's uncovered, decide whether it matters, and pay more attention to whether the tests would catch real mistakes.

## Flaky tests

A **flaky test** sometimes passes and sometimes fails with no code change. Common causes:

- **Time:** the test uses the real clock and fails near midnight, at month ends, or when the machine is slow.
- **Randomness:** a random value occasionally hits an edge case.
- **Order dependence:** a test only passes if another one ran first and left data behind.
- **Real network:** a slow or failing external service.
- **Waiting with `sleep`:** "wait 1 second for the job to finish" works until the CI machine is busy.

Every cause has the same family of fixes from the lesson "Test doubles and dependency injection": inject the clock and the random generator, give each test its own fresh state, fake the network. Treat a flaky test as a bug and fix or quarantine it quickly; a suite that "usually passes" trains everyone to ignore red.

## Running tests in CI on every pull request

**Continuous integration (CI)** means a server automatically runs your checks on every push and pull request. On GitHub this is **GitHub Actions**, configured with a YAML file in `.github/workflows/`:

```yaml
name: tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest
```

Read it top to bottom: on every push and pull request, start a fresh Ubuntu machine, check out the code, install Python 3.12 and the dependencies, run the linter, run the tests. If any step fails, the pull request shows a red ✗, and most teams block merging until it's green. This is what makes tests a team safety net rather than a personal habit: nobody can merge code that breaks them, including you on a tired Friday. You'll set this up for real in this section's project, and again when you ship software later in the course.

Keep the suite fast so CI stays fast. If unit tests take minutes, something (usually a hidden network call or a `sleep`) is wrong.

## Putting it together: how would you test this?

When someone asks how you'd test a feature, walk through it in layers:

1. **Pure logic** (calculations, validation, rules): unit tests with plenty of edge cases.
2. **Code that talks to the outside world** (database, APIs): an integration test or two for each, against a real or in-memory version.
3. **The most important user journey**: one end-to-end test.
4. **Automation**: all of it runs in CI on every pull request.

That answer, with an example of each, is what an interviewer is hoping to hear.

## Common mistakes

**Only unit tests with fakes.** Every piece works in isolation and the app is still broken where the pieces join. Add integration tests at the boundaries.

**Sharing one database across tests.** Tests start depending on each other's data and fail in confusing ways. Fresh database per test.

**Chasing a coverage number.** Tests without meaningful asserts, written to turn lines green. Ask "would this catch a bug?" instead.

**Ignoring a flaky test.** Re-running until it's green hides real failures. Find the cause: it's almost always time, randomness, shared state or the network.

**Tests that only run on your laptop.** If CI doesn't run them, they'll rot. Wire them into CI from the first commit.

## Recap

- Unit tests are many, fast and precise; integration tests check real pieces together; end-to-end tests check whole user journeys, and you only need a few.
- The test pyramid: push each test as low as it can go while still catching the bug.
- `sqlite3.connect(":memory:")` gives real, fast integration tests; use a fresh database per test and more than one row.
- Coverage shows what's untested; it doesn't prove anything is tested well.
- Fix flaky tests at the cause, and run the whole suite in CI on every pull request.
