# Logging and observability

## Why this matters

On your laptop, when something breaks you see the traceback, add a `print`, and run it again. In production you can't do any of that. The bug happened at 03:12 to a user you'll never meet, the server has no screen, and you can't re-run their request. The only evidence is what your program wrote down while it ran. Logs are that evidence. Good logs turn "the site was broken last night" into "the payment provider returned 503 for 14 minutes, here are the 212 affected orders". Bad logs, or none, turn it into guesswork.

## Why `print` isn't enough

`print` works for a ten-line script. In a running service it falls short in four ways:

- **No severity.** "user logged in" and "database unreachable" look the same. You can't show only the serious ones.
- **No context.** Which module printed it? When? For which request?
- **No control.** To silence noisy output you have to edit code. You can't send errors to one place and everything to another.
- **Wrong stream.** `print` writes to stdout, which in a command-line tool is for results, not diagnostics.

Python's standard `logging` module solves all four, and every serious Python library uses it, so learning it once pays off everywhere.

## Your first logger

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shop.orders")

logger.info("order created")
logger.debug("cart contents: 3 items")      # not shown: below INFO
logger.warning("stock low for SKU-42")
```

Output (on stderr):

```
INFO:shop.orders:order created
WARNING:shop.orders:stock low for SKU-42
```

Three things happened:

1. `basicConfig` set up logging once for the whole program: show records at level `INFO` or above, print them to stderr in a simple format.
2. `getLogger("shop.orders")` returned a **logger**, a named object you call to record events. The usual habit is `logger = logging.getLogger(__name__)` at the top of each module, so the name is the module's import path and you can tell where each line came from.
3. The `debug` call was dropped because it was below the chosen level.

> **Note:** call `basicConfig` once, at program start (in `main`), never in a library module. Library code only creates loggers and calls them; the application decides where the output goes.

## Levels: how serious is this?

Every log call has a **level**. From least to most serious:

| Level | Number | Use it for | Example |
|---|---|---|---|
| `DEBUG` | 10 | Detail you only want while investigating | `"cache miss for key user:42"` |
| `INFO` | 20 | Normal, notable events | `"order 1093 paid"`, `"server started on port 8000"` |
| `WARNING` | 30 | Something unexpected, but the program coped | `"retrying payment API (attempt 2 of 3)"` |
| `ERROR` | 40 | An operation failed | `"could not send receipt email for order 1093"` |
| `CRITICAL` | 50 | The whole program can't continue | `"cannot connect to database, shutting down"` |

The level you configure is a threshold. In development you might run at `DEBUG`; in production at `INFO`, so you get the story of what happened without drowning in detail. Remember the `LOG_LEVEL` setting from the lesson Configuration and secrets: that's exactly what it controls.

A useful test for `WARNING` vs `ERROR`: did the thing the user asked for still happen? A retry that succeeded is a warning. A receipt that never got sent is an error.

## Logging errors with the traceback

When you catch an exception, log it with `logger.exception`. It logs at `ERROR` level **and** includes the full traceback:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shop.payments")

def charge(amount):
    return 100 / amount

try:
    charge(0)
except ZeroDivisionError:
    logger.exception("charge failed for amount=%s", 0)
```

```
ERROR:shop.payments:charge failed for amount=0
Traceback (most recent call last):
  File "demo.py", line 10, in <module>
    charge(0)
  File "demo.py", line 7, in charge
    return 100 / amount
ZeroDivisionError: division by zero
```

`logger.error("failed")` without the traceback throws away the most useful line in the whole incident. Inside an `except` block, prefer `logger.exception`.

Notice the message style: `"charge failed for amount=%s", 0`. The logging module fills in `%s` itself, and only if the record will actually be shown. That's cheaper than an f-string for debug messages that are usually switched off. F-strings still work; both styles are common.

## Loggers, handlers and formatters

`basicConfig` hides some moving parts you'll need as soon as you want something custom. There are three:

```
 logger.info("order paid")
          |
          v
   +-------------+     +-------------+     +---------------+
   |   Logger    | --> |   Handler   | --> |   Formatter   | --> text written
   | name, level |     | where to    |     | how a record  |     to stderr, a
   |             |     | send it     |     | becomes text  |     file, a service
   +-------------+     +-------------+     +---------------+
```

- A **logger** creates a `LogRecord`: an object holding the level, message, logger name, time, and any extra fields.
- A **handler** decides where records go: `StreamHandler` writes to a stream such as stderr; `FileHandler` writes to a file. A logger can have several.
- A **formatter** turns a record into a line of text.

Setting them up by hand:

```python
import io
import logging

buffer = io.StringIO()
handler = logging.StreamHandler(buffer)
handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))

logger = logging.getLogger("demo")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False   # don't also pass records up to the root logger

logger.info("hello")
print(repr(buffer.getvalue()))   # 'INFO demo: hello\n'
```

Writing to an `io.StringIO` like this is also how you test logging code: attach a handler to a buffer, log, and check what came out.

## Structured (JSON) logs

A line like `INFO shop.orders: order 1093 paid by user 77 total 49.90` is easy for you to read and hard for a computer to search. "Show me every order over 40 paid by user 77" means writing a fragile regex.

**Structured logs** write each record as data, usually one JSON object per line:

```
{"time": "2026-11-13T03:12:09+00:00", "level": "INFO", "logger": "shop.orders", "message": "order paid", "order_id": 1093, "user_id": 77, "total": 49.9}
```

Log platforms (and simple tools like `jq`) can filter and group these by field. You pass the fields with `extra=`, and they become attributes on the record:

```python
logger.info("order paid", extra={"order_id": 1093, "user_id": 77, "total": 49.9})
```

The standard `Formatter` ignores those extras. To print them as JSON you write your own formatter by subclassing `logging.Formatter` and overriding `format(record)` to return a string. That's the first practice exercise. The tricky part is telling your extras apart from the two dozen built-in attributes every record has (`lineno`, `pathname`, `thread` and so on). A neat trick is to make a blank record and see which attribute names it already has:

```python
import logging

blank = logging.LogRecord("x", logging.INFO, "", 0, "", None, None)
print(sorted(blank.__dict__)[:5])   # ['args', 'created', 'exc_info', 'exc_text', 'filename']
```

Anything on a real record that isn't in that set came from `extra=`.

## Correlation IDs: following one request

A busy server handles many requests at once, so their log lines interleave. When one user reports a failure, you need *their* lines only. The fix is a **correlation ID** (or request ID): a random ID created when a request arrives, included in every log line for that request, and often returned to the user in a response header.

```
{"level": "INFO",  "message": "request started", "request_id": "a81f", "path": "/checkout"}
{"level": "INFO",  "message": "request started", "request_id": "c3d0", "path": "/cart"}
{"level": "ERROR", "message": "payment failed",  "request_id": "a81f", "status": 503}
{"level": "INFO",  "message": "request done",    "request_id": "c3d0", "status": 200}
```

Filter on `request_id == "a81f"` and the story of the failed checkout reads top to bottom. When a request calls another service, it passes the same ID along, so you can follow it across services too.

## What never to log

Logs get copied to log platforms, shared in tickets and read by many people. Treat them as semi-public. Never log:

- **passwords**, even failed ones (a user who typed their password into the username box has just logged their password),
- **tokens, API keys, session cookies and `Authorization` headers**: anyone who reads them can act as that user,
- **personal data** you don't need: full card numbers, government IDs, health details, often full email addresses and home addresses. Many countries' privacy laws (GDPR in the EU, for example) apply to logs too.

The classic way this goes wrong is logging a whole request:

```python
logger.info("login attempt", extra={"body": request_body})
# {"message": "login attempt", "body": {"email": "ada@example.com", "password": "hunter2"}}
```

Log the fields you need (`user_id`, `path`, `status`) instead of whole objects, and add a safety net that **redacts** (masks) sensitive keys before anything is written. That's the second practice exercise.

## Observability: metrics and alerts

**Observability** means being able to answer new questions about what your system is doing from the outside, without shipping new code. Logs are one part. Two others you'll hear about:

- **Metrics** are numbers measured over time: requests per second, error rate, how long requests take (latency), memory used. They're cheap to store and great for graphs: "errors jumped from 0.1% to 8% at 03:10".
- **Alerts** are rules on metrics that notify a person: "page the on-call engineer if the error rate is above 5% for 5 minutes". Alert on things users feel (errors, slowness), not on every warning line, or people learn to ignore alerts.

A third, **traces**, records how long each step of a request took across services. You don't need to set these up yet; know the words so you can follow along on a team.

## Reading logs to debug production

When an alert fires or a user reports a bug, a calm routine works:

1. **Pin down the time window** and, if possible, a request ID, user ID or order ID.
2. **Filter** to `ERROR` and above in that window. Find the first error, not the loudest; later errors are often consequences.
3. **Follow the request ID** backwards to see what happened before the error.
4. **Read the traceback** bottom-up, as you learned in the debugging lessons: the last line is what went wrong, the frames above show where.
5. **Write down what was missing.** If you couldn't answer a question from the logs, add the log line that would have answered it. Logs get better one incident at a time.

## Common mistakes

**No output at all.** If `logger.info(...)` prints nothing, the level is filtering it out: the default threshold is `WARNING`. Call `logging.basicConfig(level=logging.INFO)` in `main`.

**Every line printed twice.** You added a handler to your logger *and* the root logger has one (from `basicConfig`), so each record is written by both. Set `logger.propagate = False`, or only configure the root logger.

**`KeyError: "Attempt to overwrite 'message' in LogRecord"`.** Some names are reserved: `extra={"message": ...}` or `extra={"name": ...}` clash with built-in record attributes. Rename your field (`"msg_text"`, `"user_name"`).

**`TypeError: Object of type datetime is not JSON serializable`** in a JSON formatter. Pass `default=str` to `json.dumps` so unusual values become strings instead of crashing the logger.

**Logging and raising the same error at every level.** Each layer logs the exception and re-raises it, so one failure appears five times. Log it once, where you handle it.

> **Try it:** In the practice editor, set up a logger with a `StreamHandler` writing to an `io.StringIO`, log one `INFO` and one `DEBUG` message at level `INFO`, and print the buffer's contents. Then change the level to `DEBUG` and compare.

## Recap

- Use `logging`, not `print`: levels, names, and output you can control without editing code.
- `logger = logging.getLogger(__name__)` per module; configure handlers once in `main`.
- Pick levels by impact: `INFO` for normal events, `WARNING` when the program coped, `ERROR` when an operation failed. Use `logger.exception` inside `except` to keep the traceback.
- Loggers create records, handlers send them somewhere, formatters turn them into text.
- Structured JSON logs with fields and a correlation ID make production searchable.
- Never log passwords, tokens, auth headers or unnecessary personal data; log chosen fields and redact as a safety net.
- Metrics show trends, alerts wake people up, logs explain what happened.
