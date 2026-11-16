# Send reminders for overdue tasks

Write `send_reminders` so that it's easy to test. It needs to know the current time and it needs to send emails, two things that make tests slow and flaky. Instead of reaching out for them, it **receives them as arguments** (that's dependency injection).

```python
def send_reminders(tasks: list[dict], now: datetime, mailer) -> int: ...
```

- `tasks` is a list of dicts like
  ```python
  {"title": "Pay rent", "owner": "ada@example.com", "due": datetime(2026, 11, 1, 9, 0), "done": False}
  ```
- `now` is the current time. In real code you'd pass `datetime.now()`; in tests, a fixed time.
- `mailer` is any object with a method `send(to: str, subject: str)`. In real code it talks to an email service. The tests pass a `unittest.mock.Mock`, which records every call.

Rules:

- A task is **overdue** when it is not `done` and its `due` time is strictly **before** `now`. A task due exactly at `now` is not overdue yet.
- For every overdue task, in list order, call `mailer.send(task["owner"], "Overdue: " + task["title"])`.
- Return how many reminders were sent.

## Example

```python
from unittest.mock import Mock, call
mailer = Mock()
now = datetime(2026, 11, 13, 9, 0)
tasks = [
    {"title": "Pay rent", "owner": "ada@example.com", "due": datetime(2026, 11, 1), "done": False},
    {"title": "Book dentist", "owner": "bob@example.com", "due": datetime(2026, 12, 1), "done": False},
]
send_reminders(tasks, now, mailer)    # 1
mailer.send.call_args_list            # [call('ada@example.com', 'Overdue: Pay rent')]
```
