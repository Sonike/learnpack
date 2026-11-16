# Integration-test a SQLite repository

A **repository** is a class that hides the database behind plain methods. Unit tests with fakes can't tell you whether its SQL is right. For that you need an **integration test**: run it against a real database. SQLite's `":memory:"` database is real SQL, lives only in memory and takes about a millisecond to create, so it's perfect for this.

Write `check_repository(make_repo)` that asserts a `TaskRepository` behaves correctly.

```python
def check_repository(make_repo) -> None: ...
```

- `make_repo()` returns a **brand-new** repository connected to its own empty `:memory:` database. Call it once per scenario you test, so each scenario starts clean and can't be affected by the others.
- Return quietly if the repository is correct; raise `AssertionError` if it isn't.

The repository's promised behaviour (a working copy is in the starter so you can run your checker against it):

| Method | Promise |
|---|---|
| `add(title) -> int` | stores a new, not-done task and returns its id |
| `get(task_id) -> dict \| None` | returns `{"id": 1, "title": "Buy milk", "done": False}`, or `None` if there's no such task. `done` is a real `bool`, not `0`/`1` |
| `list() -> list[dict]` | every task as a dict like above, **in the order they were added** (by id) |
| `complete(task_id) -> bool` | marks **only that task** done and returns `True`; returns `False` if there's no such task |

The hidden tests run your checker against the correct repository (must pass) and five buggy ones (each must fail). Each bug breaks one promise in the table, so check every promise, including the "no such task" cases.

> **Tip:** to catch "complete marked the wrong rows", add **two** tasks, complete one, and check the other is still not done. One-task tests miss a lot of bugs.
