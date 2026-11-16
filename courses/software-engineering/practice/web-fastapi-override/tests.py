from fastapi.testclient import TestClient

import solution
from solution import app


class SpyRepo:
    """A fake repository that records every call and returns canned answers."""

    def __init__(self, stored=None):
        self.stored = stored or {}
        self.calls = []

    def add(self, title, body):
        self.calls.append(("add", title, body))
        return {"id": 42, "title": title, "body": body}

    def get(self, note_id):
        self.calls.append(("get", note_id))
        return self.stored.get(note_id)

    def delete(self, note_id):
        self.calls.append(("delete", note_id))
        return note_id in self.stored


def with_spy(spy, fn):
    assert hasattr(solution, "get_repo"), "solution.py needs a get_repo() function"
    app.dependency_overrides[solution.get_repo] = lambda: spy
    try:
        return fn(TestClient(app))
    finally:
        app.dependency_overrides.clear()


def test_get_repo_returns_the_real_repository():
    assert hasattr(solution, "get_repo"), "solution.py needs a get_repo() function"
    got = solution.get_repo()
    assert got is solution.repo, f"expected get_repo() to return the module's repo, got {got!r}"


def test_create_uses_the_injected_repository():
    spy = SpyRepo()
    response = with_spy(spy, lambda c: c.post("/notes", json={"title": "Hi", "body": "there"}))
    assert spy.calls == [("add", "Hi", "there")], f"expected the spy to be called, got {spy.calls!r}"
    assert response.status_code == 201, f"expected 201, got {response.status_code}"
    want = {"id": 42, "title": "Hi", "body": "there"}
    assert response.json() == want, f"expected {want!r}, got {response.json()!r}"


def test_get_uses_the_injected_repository():
    spy = SpyRepo({7: {"id": 7, "title": "Seven", "body": ""}})
    response = with_spy(spy, lambda c: c.get("/notes/7"))
    assert spy.calls == [("get", 7)], f"expected [('get', 7)], got {spy.calls!r}"
    want = {"id": 7, "title": "Seven", "body": ""}
    assert response.json() == want, f"expected {want!r}, got {response.json()!r}"


def test_missing_note_from_the_fake_is_404():
    spy = SpyRepo()
    response = with_spy(spy, lambda c: c.get("/notes/5"))
    assert response.status_code == 404, f"expected 404, got {response.status_code}"
    assert spy.calls == [("get", 5)], f"expected [('get', 5)], got {spy.calls!r}"


def test_delete_uses_the_injected_repository():
    spy = SpyRepo({3: {"id": 3, "title": "x", "body": ""}})
    statuses = with_spy(spy, lambda c: (c.delete("/notes/3").status_code, c.delete("/notes/4").status_code))
    assert statuses == (204, 404), f"expected (204, 404), got {statuses!r}"
    assert spy.calls == [("delete", 3), ("delete", 4)], f"got {spy.calls!r}"


def test_validation_still_happens_before_the_repository():
    spy = SpyRepo()
    response = with_spy(spy, lambda c: c.post("/notes", json={"title": ""}))
    assert response.status_code == 422, f"expected 422, got {response.status_code}"
    assert spy.calls == [], f"the repository shouldn't be called for invalid input, got {spy.calls!r}"
