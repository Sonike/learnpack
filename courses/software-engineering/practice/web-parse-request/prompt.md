# Parse a raw HTTP request

A web server receives a request as plain text. Write `parse_request(raw)` that turns that text into a `Request` object, the first job every web framework does for you.

```python
@dataclass
class Request:
    method: str
    path: str
    query: dict[str, str]
    headers: dict[str, str]
    body: str

def parse_request(raw: str) -> Request: ...
```

`raw` is an HTTP/1.1 request with `\r\n` line endings:

```
POST /tasks?draft=yes HTTP/1.1\r\n
Host: api.example.com\r\n
Content-Type: application/json\r\n
\r\n
{"title": "Write docs"}
```

Rules:

- **Headers and body** are separated by the first blank line (`\r\n\r\n`). If there's no body, `body` is `""`.
- The **request line** is `METHOD TARGET VERSION`. `method` is upper-cased. The target splits at `?` into `path` and the query string.
- **`query`**: `"a=1&b=2"` becomes `{"a": "1", "b": "2"}`; no query gives `{}`. You may use `urllib.parse.parse_qsl(qs, keep_blank_values=True)` or split by hand.
- **`headers`**: names are **lower-cased** (header names are case-insensitive), and spaces around names and values are stripped. Split each line at the **first** `:` only, because values can contain colons (`Host: localhost:8000`).

## Example

```python
raw = "GET /tasks?status=todo HTTP/1.1\r\nHost: localhost:8000\r\nAccept: application/json\r\n\r\n"
parse_request(raw)
# Request(method='GET', path='/tasks', query={'status': 'todo'},
#         headers={'host': 'localhost:8000', 'accept': 'application/json'}, body='')
```
