from fastapi.testclient import TestClient

from solution import app

client = TestClient(app)


def create(title, body=None):
    payload = {"title": title} if body is None else {"title": title, "body": body}
    return client.post("/notes", json=payload)


def test_create_returns_201_and_the_note():
    response = create("Groceries", "eggs, rice")
    assert response.status_code == 201, f"expected 201, got {response.status_code}: {response.text}"
    note = response.json()
    assert isinstance(note.get("id"), int), f"expected an integer id, got {note!r}"
    want = {"id": note["id"], "title": "Groceries", "body": "eggs, rice"}
    assert note == want, f"expected {want!r}, got {note!r}"


def test_body_is_optional_and_ids_increase():
    first = create("First").json()
    second = create("Second").json()
    assert first["body"] == "", f"expected body '' by default, got {first['body']!r}"
    assert second["id"] > first["id"], f"expected increasing ids, got {first['id']} then {second['id']}"


def test_get_returns_the_note_and_list_includes_it():
    note = create("Read me").json()
    response = client.get(f"/notes/{note['id']}")
    assert response.status_code == 200, f"expected 200, got {response.status_code}"
    assert response.json() == note, f"expected {note!r}, got {response.json()!r}"
    listed = client.get("/notes").json()
    assert note in listed, f"expected {note!r} in GET /notes, got {listed!r}"


def test_missing_note_is_404():
    response = client.get("/notes/999999")
    assert response.status_code == 404, f"expected 404, got {response.status_code}"
    want = {"detail": "Note not found"}
    assert response.json() == want, f"expected {want!r}, got {response.json()!r}"


def test_invalid_titles_are_422():
    for payload in [{"title": ""}, {"title": "x" * 101}, {"body": "no title"}, {"title": 42}]:
        response = client.post("/notes", json=payload)
        assert response.status_code == 422, f"{payload!r}: expected 422, got {response.status_code}"
    assert create("x" * 100).status_code == 201, "a 100-character title should be allowed"


def test_delete_returns_204_then_404():
    note = create("Temporary").json()
    response = client.delete(f"/notes/{note['id']}")
    assert response.status_code == 204, f"expected 204, got {response.status_code}"
    assert response.content == b"", f"expected an empty body, got {response.content!r}"
    assert client.get(f"/notes/{note['id']}").status_code == 404, "the note should be gone"
    assert client.delete(f"/notes/{note['id']}").status_code == 404, "deleting twice should be 404"
