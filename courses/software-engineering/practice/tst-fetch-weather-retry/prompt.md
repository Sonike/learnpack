# Retry a flaky network call

Network calls fail now and then for reasons that have nothing to do with your code. A common fix is to **retry** a few times on errors that are likely to go away, such as a timeout. Write `fetch_weather` with a retry, and keep it testable by **injecting** the function that does the network call.

```python
def fetch_weather(city: str, http_get, attempts: int = 3) -> dict: ...
```

- `city` is a city name, like `"Lagos"`.
- `http_get(url)` is the function that does the request and returns the parsed JSON as a `dict`. Real code would pass a function that uses an HTTP library; tests pass a `Mock`.
- Call it with the URL `"https://weather.example.com/today?city=" + city`.
- If `http_get` raises `TimeoutError`, try again, up to `attempts` calls **in total**. If every attempt times out, let the last `TimeoutError` propagate (don't swallow it).
- Any **other** exception (say `ValueError` for a bad response) is not worth retrying: let it propagate straight away.
- Return the dict from the first successful call.

The tests use `Mock(side_effect=[...])`: each call to the mock takes the next item from the list. If the item is an exception, the mock raises it; otherwise it returns it.

## Example

```python
from unittest.mock import Mock
http_get = Mock(side_effect=[TimeoutError, TimeoutError, {"temp_c": 31}])
fetch_weather("Lagos", http_get)   # {"temp_c": 31}
http_get.call_count                # 3
```

> **Note:** real retry code usually waits between attempts, and waits longer each time ("exponential backoff"). We leave the waiting out so the tests stay instant; if you add it later, inject a `sleep` function too.
