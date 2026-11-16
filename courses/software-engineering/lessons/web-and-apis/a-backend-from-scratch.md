# A backend from scratch

## Why this matters

Web frameworks like FastAPI, Flask and Django feel like magic: you write a decorator, and somehow an HTTP request ends up calling your function. Magic is fine until it breaks. In this lesson you'll build the core of a web framework yourself, in plain Python: a **router**, path parameters, JSON bodies, status codes, and the standard interface servers use to call Python code. After this, every framework will look like a convenient version of something you already understand, and you'll know where to look when one misbehaves.

## 1. What a backend actually does

Strip away the details and every backend does the same five things for each request:

```
   HTTP request
        |
        v
1. parse         method, path, headers, body
2. route         which function handles "GET /tasks/7"?
3. handle        run that function (validate input, do the work)
4. respond       turn the result into status + headers + body
        |
        v
   HTTP response
```

Step 0, listening on a port and reading bytes from the network, is done by a **web server** program. The framework does steps 1, 2 and 4. You write step 3. You built pieces of 1 and 4 by hand in *HTTP in depth*; now let's do routing.

## 2. Routing: from method and path to a function

A **route** is a rule: "requests with this method and this path go to this function". The function is called a **handler**. The simplest router is a dictionary:

```python
def list_tasks():
    return 200, [{"id": 1, "title": "Write tests"}]

def create_task():
    return 201, {"id": 2, "title": "Ship it"}

routes = {
    ("GET", "/tasks"): list_tasks,
    ("POST", "/tasks"): create_task,
}

handler = routes.get(("GET", "/tasks"))
print(handler())
# (200, [{'id': 1, 'title': 'Write tests'}])
```

Each handler returns a `(status, body)` pair, and something else turns that into HTTP. This already works for fixed paths. But what about `/tasks/7`, `/tasks/8`, `/tasks/9000`? We can't list every id.

## 3. Path parameters

Frameworks let you write a **pattern** with placeholders: `/tasks/{id}`. A request for `/tasks/7` matches it, with `id = "7"`. Here's how to match one pattern against one path, by splitting both on `/` and comparing piece by piece:

```python
def match(pattern: str, path: str) -> dict | None:
    pattern_parts = pattern.strip("/").split("/")
    path_parts = path.strip("/").split("/")
    if len(pattern_parts) != len(path_parts):
        return None
    params = {}
    for want, got in zip(pattern_parts, path_parts):
        if want.startswith("{") and want.endswith("}"):
            params[want[1:-1]] = got          # a placeholder: capture the value
        elif want != got:
            return None                       # a fixed piece that doesn't match
    return params

print(match("/tasks/{id}", "/tasks/7"))             # {'id': '7'}
print(match("/tasks/{id}", "/tasks"))               # None  (different length)
print(match("/users/{uid}/tasks/{tid}", "/users/3/tasks/9"))
# {'uid': '3', 'tid': '9'}
print(match("/tasks/{id}", "/users/7"))             # None  ("tasks" != "users")
```

Captured values are always **strings**, because a URL is text. Converting `"7"` to `7`, and answering 404 when it isn't a number, is the handler's job. (FastAPI does it for you based on type hints, as you'll see in *Building an API with FastAPI*.)

## 4. 404 vs 405

When no route matches, there are two different answers:

- **404 Not Found**: no route has this path at all, e.g. `GET /banana`.
- **405 Method Not Allowed**: the path exists, but not with this method, e.g. `DELETE /tasks` when only `GET` and `POST` are defined.

A careful router checks every route: if some route's pattern matched the path but the method was wrong, remember that, and answer 405 instead of 404 at the end. That's exactly what you'll build in the first exercise.

## 5. WSGI: how servers call Python

A web server (the program that owns the port) needs a standard way to hand a request to your Python code. For Python, that standard is **WSGI** (Web Server Gateway Interface, said "wiz-ghee"). It's tiny. A WSGI app is any function with this shape:

```python
def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Hello from WSGI\n"]
```

- **`environ`** is a dict describing the request. The keys you need most:

  | Key | Example |
  |---|---|
  | `REQUEST_METHOD` | `"GET"` |
  | `PATH_INFO` | `"/tasks/7"` |
  | `QUERY_STRING` | `"status=todo"` (without the `?`) |
  | `CONTENT_LENGTH` | `"27"` (a string; may be missing or empty) |
  | `wsgi.input` | a file-like object: read the body bytes from it |

- **`start_response(status, headers)`** is a function the server gives you. Call it once with the status line text and a list of `(name, value)` header tuples.
- The **return value** is a list (any iterable) of `bytes`: the body.

Flask and Django are WSGI apps underneath. (FastAPI uses **ASGI**, the async successor, but the idea is the same.)

To try one in your browser locally, the standard library includes a simple server:

```python
from wsgiref.simple_server import make_server

with make_server("localhost", 8000, app) as server:
    print("Serving on http://localhost:8000")
    server.serve_forever()            # Ctrl+C to stop
```

> **Note:** this server is for learning and local experiments only; it's slow and handles one request at a time. Run it on your own machine, not in the practice editor (the browser version can't open ports). Production uses servers like Gunicorn or Uvicorn.

## 6. Testing a WSGI app without a server

Because a WSGI app is just a function, you can test it by calling it with a hand-built `environ`. `wsgiref.util.setup_testing_defaults` fills in all the boring keys for you:

```python
import io
import json
from wsgiref.util import setup_testing_defaults

def call(app, method, path, body=None):
    raw = json.dumps(body).encode("utf-8") if body is not None else b""
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(raw)),
        "wsgi.input": io.BytesIO(raw),
    }
    setup_testing_defaults(environ)        # adds SERVER_NAME, wsgi.version, ...
    captured = {}
    def start_response(status, headers):
        captured["status"], captured["headers"] = status, headers
    chunks = app(environ, start_response)
    return captured["status"], b"".join(chunks).decode("utf-8")

print(call(app, "GET", "/"))
# ('200 OK', 'Hello from WSGI\n')
```

No ports, no network, and it runs in a millisecond. `io.BytesIO(raw)` wraps bytes in a file-like object, standing in for the network connection. The practice tests use exactly this approach.

## 7. A tiny JSON API, end to end

Putting the pieces together: read the method and path, read and parse the JSON body, route, call the handler, and send JSON back.

```python
import json
from http import HTTPStatus

TASKS = {1: {"id": 1, "title": "Write tests"}}

def app(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ.get("PATH_INFO", "/")

    if method == "GET" and path == "/tasks":
        status, body = 200, list(TASKS.values())
    elif method == "POST" and path == "/tasks":
        length = int(environ.get("CONTENT_LENGTH") or 0)
        try:
            data = json.loads(environ["wsgi.input"].read(length) or b"null")
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, dict) or not str(data.get("title", "")).strip():
            status, body = 400, {"error": "title is required"}
        else:
            new_id = max(TASKS, default=0) + 1
            TASKS[new_id] = {"id": new_id, "title": data["title"].strip()}
            status, body = 201, TASKS[new_id]
    else:
        status, body = 404, {"error": "not found"}

    payload = json.dumps(body).encode("utf-8")
    start_response(
        f"{status} {HTTPStatus(status).phrase}",
        [("Content-Type", "application/json"), ("Content-Length", str(len(payload)))],
    )
    return [payload]

print(call(app, "POST", "/tasks", {"title": "Ship it"}))
# ('201 Created', '{"id": 2, "title": "Ship it"}')
print(call(app, "POST", "/tasks", {"title": ""}))
# ('400 Bad Request', '{"error": "title is required"}')
```

Notice how much of this is plumbing: reading `CONTENT_LENGTH`, decoding JSON, handling bad JSON, building the status line, encoding the response. That plumbing is what frameworks do for you. Notice too that the routing is a growing `if/elif` chain, which is why we want a proper router.

## 8. Layers: handler, service, repository

Look at the `POST` branch above: it parses input, validates it, decides the new id, and stores data, all in one place. As apps grow, that becomes a tangle. The standard fix is to split the code into **layers**, each with one job:

```
HTTP request
    |
handler      knows HTTP: parse the request, pick a status code, format JSON
    |
service      knows the rules: "a title can't be empty", "only the owner can edit"
    |
repository   knows SQL: INSERT, SELECT, UPDATE  (from "SQL from Python, safely")
    |
database
```

Each layer only talks to the one below it. Why bother?

- **Testability.** You can test the rules in the service without HTTP, and test the handler with a fake repository and no database.
- **Change one thing at a time.** Moving from SQLite to PostgreSQL touches only the repository. Switching from WSGI to FastAPI touches only the handlers.
- **No SQL in handlers.** If SQL is scattered through your handlers, every change to the schema means hunting through HTTP code, and it's much easier to slip in an injectable query.

For small apps, the service layer can be thin or merged into the handler. Keep the repository separate from the start, though; it's cheap and pays off immediately. The second practice exercise does exactly that: a WSGI API whose handlers call a `TaskRepository`, and the repository is handed to the app from outside so each test gets a fresh one.

## Common mistakes

**Returning `str` instead of `bytes` from a WSGI app.** The server raises something like `AssertionError: write() argument must be a bytes instance`. Encode with `.encode("utf-8")` and return a list: `[payload]`.

**Calling `start_response` with an int.** The status must be text like `"404 Not Found"`, not `404`.

**`int(environ["CONTENT_LENGTH"])` crashing.** The key may be missing or an empty string for requests without a body. Use `int(environ.get("CONTENT_LENGTH") or 0)`.

**Forgetting path parameters are strings.** `tasks.get("7")` finds nothing when the keys are ints. Convert, and answer 404 for values like `"abc"` instead of crashing with a `ValueError` (which becomes a 500).

**Reading the body twice.** `wsgi.input` is a stream: once read, it's empty. Read it once and keep the bytes.

## Recap

- Every backend: **parse → route → handle → respond**. Frameworks do the parsing, routing and responding; you write handlers.
- A **route** maps a method and a path **pattern** like `/tasks/{id}` to a **handler**; captured path parameters are strings.
- No path match → **404**; path matches but wrong method → **405**.
- **WSGI**: `app(environ, start_response)` returns a list of bytes. You can test it by calling it directly with a built `environ`.
- Split code into **handler → service → repository** so each layer is simple and testable, and SQL stays out of handlers.
