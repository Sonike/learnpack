import io
import json
import sqlite3
from wsgiref.util import setup_testing_defaults

from solution import TaskRepository, make_app


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


def fresh():
    return make_app(TaskRepository(sqlite3.connect(":memory:")))


def test_post_creates_a_task_with_201():
    status, headers, body = call(fresh(), "POST", "/tasks", {"title": "Ship it"})
    assert status == "201 Created", f"expected '201 Created', got {status!r}"
    want = {"id": 1, "title": "Ship it", "status": "todo"}
    assert body == want, f"expected {want!r}, got {body!r}"
    assert headers.get("Content-Type") == "application/json", f"expected a JSON Content-Type, got {headers!r}"


def test_get_lists_all_tasks():
    app = fresh()
    call(app, "POST", "/tasks", {"title": "a"})
    call(app, "POST", "/tasks", {"title": "b"})
    status, _, body = call(app, "GET", "/tasks")
    want = [{"id": 1, "title": "a", "status": "todo"}, {"id": 2, "title": "b", "status": "todo"}]
    assert status == "200 OK", f"expected '200 OK', got {status!r}"
    assert body == want, f"expected {want!r}, got {body!r}"


def test_get_one_task_or_404():
    app = fresh()
    call(app, "POST", "/tasks", {"title": "a"})
    status, _, body = call(app, "GET", "/tasks/1")
    assert (status, body) == ("200 OK", {"id": 1, "title": "a", "status": "todo"}), f"got {status!r} {body!r}"
    for path in ["/tasks/99", "/tasks/abc"]:
        status, _, body = call(app, "GET", path)
        assert status == "404 Not Found", f"GET {path}: expected '404 Not Found', got {status!r}"
        assert "error" in body, f"GET {path}: expected an 'error' key, got {body!r}"


def test_bad_post_bodies_are_400():
    app = fresh()
    for raw in [b"not json", b"[1, 2]", json.dumps({}).encode(), json.dumps({"title": "  "}).encode(),
                json.dumps({"title": 42}).encode(), b""]:
        status, _, body = call(app, "POST", "/tasks", raw)
        assert status == "400 Bad Request", f"body {raw!r}: expected '400 Bad Request', got {status!r}"
        assert "error" in body, f"body {raw!r}: expected an 'error' key, got {body!r}"
    _, _, tasks = call(app, "GET", "/tasks")
    assert tasks == [], f"no task should have been stored, got {tasks!r}"


def test_unknown_path_is_404_and_wrong_method_is_405():
    app = fresh()
    status, _, _ = call(app, "GET", "/banana")
    assert status == "404 Not Found", f"expected '404 Not Found', got {status!r}"
    for method, path in [("DELETE", "/tasks"), ("PUT", "/tasks/1")]:
        status, _, _ = call(app, method, path)
        assert status == "405 Method Not Allowed", f"{method} {path}: expected '405 Method Not Allowed', got {status!r}"


def test_content_length_matches_the_body_bytes():
    app = fresh()
    raw = json.dumps({"title": "Café ☕"}, ensure_ascii=False).encode("utf-8")
    environ = {"REQUEST_METHOD": "POST", "PATH_INFO": "/tasks",
               "CONTENT_LENGTH": str(len(raw)), "wsgi.input": io.BytesIO(raw)}
    setup_testing_defaults(environ)
    seen = {}
    payload = b"".join(app(environ, lambda status, headers: seen.update(dict(headers))))
    want = str(len(payload))
    assert seen.get("Content-Length") == want, f"expected Content-Length {want!r}, got {seen.get('Content-Length')!r}"
    got = json.loads(payload)["title"]
    assert got == "Café ☕", f"expected {'Café ☕'!r}, got {got!r}"
