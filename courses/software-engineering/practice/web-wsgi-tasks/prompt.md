# A tasks API in plain WSGI

Write `make_app(repo)`: a function that returns a **WSGI app** (a function `app(environ, start_response)`) serving a small JSON tasks API. The app gets all its data through `repo`, a `TaskRepository` (given in the starter, the same one you built in *SQL from Python, safely*), so the handlers contain no SQL.

```python
def make_app(repo: TaskRepository): ...   # returns app(environ, start_response)
```

Taking `repo` as an argument means each test can hand the app a fresh in-memory database.

| Request | Response |
|---|---|
| `GET /tasks` | `200`, a JSON list of all tasks: `[{"id": 1, "title": "...", "status": "todo"}, ...]` |
| `POST /tasks` with body `{"title": "Ship it"}` | `201`, the new task as JSON |
| `POST /tasks` with invalid JSON, a body that isn't an object, or a missing/empty/non-text `title` | `400`, `{"error": "<a message>"}` |
| `GET /tasks/{id}` | `200` and the task, or `404` `{"error": ...}` if there's no such task **or the id isn't a number** |
| any other path | `404` `{"error": ...}` |
| a known path with another method (e.g. `DELETE /tasks`) | `405` `{"error": ...}` |

Every response:

- calls `start_response` with a status like `"201 Created"` (use `HTTPStatus(code).phrase`) and the headers `Content-Type: application/json` and `Content-Length` (in bytes);
- returns a list holding the JSON body as **bytes**.

From `environ` you need `REQUEST_METHOD`, `PATH_INFO`, `CONTENT_LENGTH` (may be `""`) and `wsgi.input` (read the body bytes from it). `dataclasses.asdict(task)` turns a `Task` into a dict.

The starter includes `call(app, method, path, body)`, the same helper the tests use, so you can try requests without a server.

## Example

```python
app = make_app(TaskRepository(sqlite3.connect(":memory:")))
call(app, "POST", "/tasks", {"title": "Ship it"})
# ('201 Created', {...headers...}, {'id': 1, 'title': 'Ship it', 'status': 'todo'})
call(app, "GET", "/tasks/abc")
# ('404 Not Found', {...}, {'error': 'task not found'})
```
