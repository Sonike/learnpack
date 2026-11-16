# Retry with exponential backoff

Write `call_with_retry(fn, retries, sleep, base_delay)` that retries temporary API failures, waiting longer after each one.

```python
def call_with_retry(fn, retries: int = 3, sleep=time.sleep, base_delay: float = 1.0) -> dict: ...
```

- `fn()` makes one request and returns a response dict with at least a `"status"` key, e.g. `{"status": 200, "data": [...]}`.
- `retries`: how many times to **retry** after the first attempt. So `fn` is called at most `retries + 1` times.
- `sleep(seconds)`: the function used to wait. Tests pass a fake that records the delays instead of waiting.
- `base_delay`: the first wait, in seconds.

Rules:

1. Call `fn()`. If the status is **not** 429 or 503, return the response straight away. That includes successes **and** errors like 400, 401 or 404, which retrying won't fix.
2. If it is 429 or 503 and you still have retries left, wait, then try again. The waits double each time: `base_delay * 2 ** attempt` for attempt 0, 1, 2… (so 1, 2, 4 with the defaults).
3. If the response has a `"retry_after"` key (the server saying how many seconds to wait), wait **that** long instead.
4. When retries run out, return the last response (don't sleep after the final attempt).

## Example

```python
responses = iter([{"status": 503}, {"status": 429}, {"status": 200, "data": "ok"}])
waits = []
call_with_retry(lambda: next(responses), sleep=waits.append)
# {'status': 200, 'data': 'ok'}
waits
# [1.0, 2.0]
```
