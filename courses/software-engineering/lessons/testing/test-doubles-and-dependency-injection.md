# Test doubles and dependency injection

## Why this matters

Real programs read the clock, roll random numbers, call web APIs, send emails and write files. Tests that touch those things are slow, break when the Wi-Fi drops, pass on Monday and fail on Tuesday, and might email real customers. The fix has two halves: design code so these outside dependencies are **passed in** (dependency injection), then pass in harmless stand-ins (test doubles) during tests. It's one of the most important skills for writing testable code, and interviewers ask about it often.

## The problem: hidden dependencies

Here's a function that sends reminders for overdue tasks:

```python
from datetime import datetime


def send_reminders(tasks):
    now = datetime.now()
    for task in tasks:
        if not task["done"] and task["due"] < now:
            email_service.send(task["owner"], "Overdue: " + task["title"])
```

Try to test it. What does "overdue" mean? It depends on the real time when the test runs, so a test with a task due "next Friday" passes today and fails next Saturday. And every run sends real emails through `email_service`. The function has **hidden dependencies**: things it reaches out and grabs, which a test can't control.

Things that make tests unreliable:

| Dependency | Why it hurts tests |
|---|---|
| The clock (`datetime.now()`, `time.time()`) | The answer changes every time you run |
| Randomness (`random`) | Different result each run |
| Network (APIs, email, payments) | Slow, can fail for unrelated reasons, has real side effects |
| Files and databases | Leftover state between runs, permissions, cleanup |

A test that sometimes passes and sometimes fails without any code change is called **flaky**. Flaky tests are poison: people learn to ignore failures, and then they ignore a real one.

## Dependency injection: pass it in

**Dependency injection** is a fancy name for a simple idea: instead of a function reaching out for what it needs, it receives it as a parameter.

```python
from datetime import datetime


def send_reminders(tasks, now, mailer):
    sent = 0
    for task in tasks:
        if not task["done"] and task["due"] < now:
            mailer.send(task["owner"], "Overdue: " + task["title"])
            sent += 1
    return sent
```

Real code calls it with the real things:

```python
send_reminders(tasks, datetime.now(), SmtpMailer())
```

Tests call it with things they control: a fixed time and a fake mailer. The function doesn't know or care which it gets. It just needs a `now` that compares with dates and a `mailer` with a `send` method (duck typing again, from the lesson "Inheritance, composition and interfaces").

The same idea works for classes, by passing dependencies to `__init__`:

```python
class ReminderService:
    def __init__(self, mailer, clock):
        self.mailer = mailer
        self.clock = clock          # a function that returns the current time

    def run(self, tasks):
        return send_reminders(tasks, self.clock(), self.mailer)
```

In real code: `ReminderService(SmtpMailer(), datetime.now)`. Note `datetime.now` without parentheses: we pass the function itself, so the service can call it whenever it needs the time. In tests: `ReminderService(fake_mailer, lambda: datetime(2026, 11, 13, 9, 0))`.

## Test doubles: fakes, stubs and mocks

A **test double** is anything that stands in for a real dependency during a test (like a stunt double in a film). There are a few kinds, and the names come up in code reviews and interviews:

- A **stub** returns canned answers. "Whatever you ask, the temperature is 31." It lets the code under test run, and you check the code's *output*.
- A **fake** is a working, simplified implementation. An in-memory dict instead of a database; a mailer that appends messages to a list instead of sending them. You can check its *state* afterwards ("is there one message in the outbox?").
- A **mock** records how it was called, so the test can check the *interaction*: "was `send` called exactly once, with these arguments?"

Here's a hand-written fake mailer:

```python
from datetime import datetime


class FakeMailer:
    def __init__(self):
        self.sent = []

    def send(self, to, subject):
        self.sent.append((to, subject))


def test_overdue_task_gets_a_reminder():
    mailer = FakeMailer()
    now = datetime(2026, 11, 13, 9, 0)
    tasks = [{"title": "Pay rent", "owner": "ada@example.com", "due": datetime(2026, 11, 1), "done": False}]

    send_reminders(tasks, now, mailer)

    assert mailer.sent == [("ada@example.com", "Overdue: Pay rent")]
```

The test is fast, gives the same answer every time, and sends no real email. Fakes are often the clearest choice: simple, readable, reusable across many tests.

## `unittest.mock`

Python's standard library has a ready-made mock in `unittest.mock`. A `Mock` object accepts any method call and records it:

```python
from unittest.mock import Mock, call

mailer = Mock()
mailer.send("ada@example.com", "Overdue: Pay rent")

print(mailer.send.call_count)        # 1
print(mailer.send.call_args)         # call('ada@example.com', 'Overdue: Pay rent')
mailer.send.assert_called_once_with("ada@example.com", "Overdue: Pay rent")   # passes silently
print(mailer.send.call_args_list == [call("ada@example.com", "Overdue: Pay rent")])   # True
```

`mailer.send` didn't exist until we called it: a `Mock` invents attributes on demand. That makes mocks quick to set up, and also makes them dangerous with typos (more below).

Mocks can be stubs too. `return_value` sets what a call returns, and `side_effect` sets a sequence of results, where any exception in the list is raised instead of returned:

```python
from unittest.mock import Mock

http_get = Mock(return_value={"temp_c": 31})
print(http_get("https://weather.example.com/today?city=Lagos"))   # {'temp_c': 31}

flaky = Mock(side_effect=[TimeoutError, {"temp_c": 31}])
try:
    flaky("url")
except TimeoutError:
    print("first call timed out")      # first call timed out
print(flaky("url"))                     # {'temp_c': 31}
```

`side_effect` is perfect for testing retry logic, as you'll see in the practice exercise: "fail twice, then succeed" becomes one line.

## `patch`: replacing something you can't inject

Sometimes code you need to test calls a dependency directly and you can't change its signature yet. `unittest.mock.patch` temporarily replaces a name while a block runs:

```python
from unittest.mock import patch


def greet():
    print("hello")


with patch("builtins.print") as fake_print:
    greet()

print(fake_print.call_args)   # call('hello')
```

Inside the `with` block, `print` is a mock; afterwards it's restored. The string is the **import path of the name where it's looked up**. If `reports.py` does `from datetime import datetime` and calls `datetime.now()`, you'd patch `"reports.datetime"`, not `"datetime.datetime"`. Getting this path wrong is the most common `patch` bug: the patch silently replaces the wrong thing and the real dependency still runs.

`patch` is useful for legacy code, but treat it as a sign that dependency injection would be cleaner. Patching the clock or the network everywhere ties your tests to the exact way the code imports things, so the tests break when someone tidies an import, even though behaviour didn't change.

## Don't mock what you don't own

If your code talks to a third-party library (a payments SDK, an HTTP client), resist mocking that library's methods directly in every test. Its API is complicated, and your mocks will drift from how it really behaves, so tests pass while production fails.

Instead, **wrap** it in a small class of your own with exactly the methods your app needs:

```python
class WeatherClient:
    """The only place that knows about the real HTTP library."""

    def __init__(self, http_get):
        self.http_get = http_get

    def temperature(self, city: str) -> float:
        data = self.http_get("https://weather.example.com/today?city=" + city)
        return data["temp_c"]
```

The rest of your code depends on `WeatherClient.temperature`, a tiny interface you control and can fake easily. `WeatherClient` itself gets a few integration tests against the real thing (see the lesson "Testing strategy"). This is called an **adapter**, and it's composition again.

## Choosing a double

| Situation | Good choice |
|---|---|
| You care about the result your code produces, and the dependency just supplies data | a **stub** (`Mock(return_value=...)`) |
| Many tests need a working stand-in, like an in-memory repository | a **fake** class |
| The *point* of the code is the call itself: sending an email, charging a card | a **mock**, and assert how it was called |
| Simulating failures: timeouts, errors, then success | `Mock(side_effect=[...])` |
| Legacy code that grabs a dependency directly | `patch`, then refactor towards injection |

## Common mistakes

**Typos on mocks pass silently.** A plain `Mock` accepts any attribute, so `mailer.sned(...)` (a typo for `send`) just records a call to a method that doesn't exist, and the test may still pass. Python does catch misspelled assertions: `mailer.send.assert_caled_once()` raises `AttributeError: 'assert_caled_once' is not a valid assertion`. `Mock(spec=RealMailer)` rejects any attribute the real class doesn't have.

**Patching the wrong path.** Patch where the name is *used*, not where it's defined. If your patch seems to have no effect, this is why.

**Mocking everything.** A test where every collaborator is a mock often just repeats the implementation ("calls A, then B, then C") and breaks on every refactor. Mock at the edges (clock, network, email), and use real objects for your own plain logic.

**Fixed dates that hide boundary bugs.** Test "due exactly now" as well as "due yesterday" and "due tomorrow". With an injected `now`, boundary tests are trivial to write.

**Calling `datetime.now()` deep inside logic.** If you find yourself wanting to patch the clock, pass `now` in instead.

## Recap

- The clock, randomness, network and files make tests slow and flaky.
- **Dependency injection**: pass dependencies in as arguments, so tests can pass in controlled ones.
- **Test doubles**: stubs return canned data, fakes are simple working versions, mocks record calls for you to check.
- `unittest.mock.Mock` with `return_value`, `side_effect` and `assert_called_once_with`; `patch` for code you can't inject into yet.
- Wrap third-party libraries in your own small adapter and fake that, rather than mocking what you don't own.
