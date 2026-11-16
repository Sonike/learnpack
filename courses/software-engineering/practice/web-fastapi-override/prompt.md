# Inject the repository with Depends

The notes API in the starter works, but its handlers reach straight for a global `repo` object. That makes them impossible to test without the real storage. Refactor it so FastAPI **injects** the repository, and tests can swap in a fake with `app.dependency_overrides`.

You need to:

1. Write `get_repo() -> NoteRepository` that returns the module's `repo` object.
2. Change all three handlers to receive the repository as a parameter, `repo: NoteRepository = Depends(get_repo)`, and use **only that parameter**, never the global.

Keep the endpoints' behaviour the same:

| Endpoint | Calls | Responds |
|---|---|---|
| `POST /notes` with `{"title", "body"}` | `repo.add(title, body)` | **201** and what `add` returned |
| `GET /notes/{note_id}` | `repo.get(note_id)` | **200** and the note, or **404** `{"detail": "Note not found"}` if it returned `None` |
| `DELETE /notes/{note_id}` | `repo.delete(note_id)` | **204**, or **404** `{"detail": "Note not found"}` if it returned `False` |

The tests do this:

```python
spy = SpyRepo()                                  # a fake that records every call
app.dependency_overrides[get_repo] = lambda: spy
client.post("/notes", json={"title": "Hi"})
assert spy.calls == [("add", "Hi", "")]
```

If a handler still uses the global `repo`, the spy never sees the call and the test fails.

## Example

```python
def get_repo() -> NoteRepository:
    return repo

@app.get("/notes/{note_id}")
def get_note(note_id: int, repo: NoteRepository = Depends(get_repo)):
    ...
```
