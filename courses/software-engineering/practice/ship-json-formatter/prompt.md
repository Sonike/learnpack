# A JSON log formatter

Write a `logging.Formatter` subclass that turns each log record into **one line of JSON**, so log tools can search by field.

```python
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ...
```

`format` receives a `LogRecord` (the object the logging module creates for each log call) and must return a string: a JSON object with these keys, in this order:

1. `"time"`: when the record was created, as an ISO 8601 string in UTC. `record.created` is a Unix timestamp; use `datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()`.
2. `"level"`: `record.levelname`, such as `"INFO"`.
3. `"logger"`: `record.name`.
4. `"message"`: `record.getMessage()` (this fills in `%s` arguments).
5. **Every extra field** passed with `extra={...}`, with its own key and value, in the order given.
6. `"exception"`: only if the record has exception info (`record.exc_info` is truthy, as it is for `logger.exception(...)`). The value is `self.formatException(record.exc_info)`, the traceback as text.

Use `json.dumps(..., default=str)` so values JSON can't handle (like a `datetime`) become strings instead of crashing.

**How to find the extras:** a record has many built-in attributes. Make a blank record once and keep its attribute names:

```python
STANDARD = set(logging.LogRecord("x", logging.INFO, "", 0, "", None, None).__dict__) | {"message", "asctime"}
```

Any key in `record.__dict__` that isn't in `STANDARD` is an extra.

## Example

```python
import io, logging
buffer = io.StringIO()
handler = logging.StreamHandler(buffer)
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("shop.orders")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("order %s paid", 1093, extra={"user_id": 77, "total": 49.9})
print(buffer.getvalue())
# {"time": "2026-11-13T03:12:09.123456+00:00", "level": "INFO", "logger": "shop.orders", "message": "order 1093 paid", "user_id": 77, "total": 49.9}
```
