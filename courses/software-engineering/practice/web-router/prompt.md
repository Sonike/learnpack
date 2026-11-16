# Build a router

Build the heart of a web framework: a `Router` that maps a method and a path pattern to a handler function, and finds the right handler for each request.

```python
class Router:
    def add(self, method: str, pattern: str, handler) -> None: ...
    def dispatch(self, method: str, path: str) -> tuple[int, object]: ...
```

- **`add(method, pattern, handler)`** registers a route. `pattern` can contain placeholders in braces: `"/tasks/{id}"`, `"/users/{uid}/tasks/{tid}"`.
- **`dispatch(method, path)`** finds the first route whose method and pattern match, calls its handler with the captured placeholders as **keyword arguments** (values are strings), and returns whatever the handler returns. Handlers return a `(status, body)` tuple.

Matching rules:

- Split pattern and path on `/` (ignore leading and trailing slashes). They match if they have the same number of pieces and every fixed piece is equal; a `{name}` piece matches anything and captures it.
- Methods are compared case-insensitively (`"get"` == `"GET"`).
- If no route's pattern matches the path, return `(404, {"error": "Not Found"})`.
- If some route's pattern matches but none with this method, return `(405, {"error": "Method Not Allowed"})`.

## Example

```python
router = Router()
router.add("GET", "/tasks", lambda: (200, ["all tasks"]))
router.add("GET", "/tasks/{id}", lambda id: (200, {"id": id}))

router.dispatch("GET", "/tasks/7")      # (200, {'id': '7'})
router.dispatch("DELETE", "/tasks/7")   # (405, {'error': 'Method Not Allowed'})
router.dispatch("GET", "/banana")       # (404, {'error': 'Not Found'})
```
