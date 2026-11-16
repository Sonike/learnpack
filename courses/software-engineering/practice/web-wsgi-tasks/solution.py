import io
import json
import sqlite3
from dataclasses import asdict, dataclass
from http import HTTPStatus
from wsgiref.util import setup_testing_defaults


# ---- The repository from "SQL from Python, safely" (given: don't change it) ----

@dataclass
class Task:
    id: int
    title: str
    status: str


class TaskRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, "
                "title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'todo')"
            )

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        with self.conn:
            cur = self.conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        return Task(cur.lastrowid, title, "todo")

    def get(self, task_id: int) -> Task | None:
        row = self.conn.execute("SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return Task(*row) if row else None

    def list(self, status: str | None = None) -> list[Task]:
        rows = self.conn.execute("SELECT id, title, status FROM tasks ORDER BY id")
        return [Task(*row) for row in rows]


# ---- Your code ----

def read_json(environ):
    """The request body parsed as JSON, or None if it isn't valid JSON."""
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw = environ["wsgi.input"].read(length)
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def make_app(repo: TaskRepository):
    """Return a WSGI app serving GET/POST /tasks and GET /tasks/{id}."""

    def list_tasks(environ):
        return 200, [asdict(task) for task in repo.list()]

    def create_task(environ):
        data = read_json(environ)
        if not isinstance(data, dict):
            return 400, {"error": "body must be a JSON object"}
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return 400, {"error": "title is required"}
        return 201, asdict(repo.add(title))

    def get_task(environ, task_id):
        if not task_id.isdigit():
            return 404, {"error": "task not found"}
        task = repo.get(int(task_id))
        if task is None:
            return 404, {"error": "task not found"}
        return 200, asdict(task)

    def route(environ):
        method = environ["REQUEST_METHOD"].upper()
        parts = environ.get("PATH_INFO", "/").strip("/").split("/")
        if parts == ["tasks"]:
            if method == "GET":
                return list_tasks(environ)
            if method == "POST":
                return create_task(environ)
            return 405, {"error": "method not allowed"}
        if len(parts) == 2 and parts[0] == "tasks":
            if method == "GET":
                return get_task(environ, parts[1])
            return 405, {"error": "method not allowed"}
        return 404, {"error": "not found"}

    def app(environ, start_response):
        status, body = route(environ)
        payload = json.dumps(body).encode("utf-8")
        start_response(f"{status} {HTTPStatus(status).phrase}",
                       [("Content-Type", "application/json"), ("Content-Length", str(len(payload)))])
        return [payload]

    return app


def call(app, method, path, body=b""):
    """Send one request to a WSGI app without a server. Returns (status, headers, decoded JSON)."""
    if isinstance(body, (dict, list)):
        body = json.dumps(body).encode("utf-8")
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path,
               "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body)}
    setup_testing_defaults(environ)
    captured = {}

    def start_response(status, headers):
        captured["status"], captured["headers"] = status, dict(headers)

    raw = b"".join(app(environ, start_response))
    return captured["status"], captured["headers"], json.loads(raw)


if __name__ == "__main__":
    app = make_app(TaskRepository(sqlite3.connect(":memory:")))
    print(call(app, "POST", "/tasks", {"title": "Ship it"}))
    print(call(app, "GET", "/tasks"))
