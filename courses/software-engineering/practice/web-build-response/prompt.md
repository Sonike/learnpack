# Build a raw HTTP response

Write `build_response(status, body)` that returns the complete text of an HTTP/1.1 JSON response.

```python
def build_response(status: int, body: dict) -> str: ...
```

- `status`: an HTTP status code such as `200`, `201` or `404`.
- `body`: a dict to send as JSON.

The response must look exactly like this, with `\r\n` line endings:

```
HTTP/1.1 404 Not Found\r\n
Content-Type: application/json\r\n
Content-Length: 25\r\n
\r\n
{"error": "no such task"}
```

- The **status line** is `HTTP/1.1 <code> <reason>`. Get the reason phrase from `http.HTTPStatus(status).phrase` (`404` → `"Not Found"`).
- Encode the body with `json.dumps(body, ensure_ascii=False)`, so non-English text is sent as real UTF-8 characters.
- **`Content-Length` is the number of bytes**, not characters: `len(text.encode("utf-8"))`. `"café"` is 4 characters but 5 bytes. A test checks this.
- Exactly these two headers, in this order, then a blank line, then the body.

## Example

```python
build_response(201, {"id": 7})
# 'HTTP/1.1 201 Created\r\nContent-Type: application/json\r\nContent-Length: 9\r\n\r\n{"id": 7}'
```
