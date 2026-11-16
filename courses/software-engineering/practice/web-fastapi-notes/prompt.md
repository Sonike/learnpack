# A notes API with FastAPI

Build a small CRUD API for notes with FastAPI. FastAPI and Pydantic do the parsing and validation; you describe the data and write the handlers.

Your `solution.py` must define `app = FastAPI()` and these two Pydantic models:

```python
class NoteIn(BaseModel):      # what clients send
    title: str                # 1 to 100 characters (use Field(min_length=..., max_length=...))
    body: str = ""

class Note(BaseModel):        # what the API returns
    id: int
    title: str
    body: str
```

| Endpoint | Success | Errors |
|---|---|---|
| `POST /notes` with a `NoteIn` body | **201** and the new `Note` (ids start at 1 and go up) | **422** if the body is invalid (FastAPI does this for you) |
| `GET /notes` | **200** and a list of all notes, oldest first | |
| `GET /notes/{note_id}` | **200** and the `Note` | **404** with `{"detail": "Note not found"}` |
| `DELETE /notes/{note_id}` | **204** with an empty body | **404** with `{"detail": "Note not found"}` |

Store notes in memory, in a module-level dict (`NOTES: dict[int, dict] = {}`), with a counter for the next id.

Hints: `status_code=201` / `status_code=204` on the decorator, `response_model=Note` (or `list[Note]`), and `raise HTTPException(status_code=404, detail="Note not found")`. Use plain `def` handlers.

The tests use `fastapi.testclient.TestClient`. The starter's `__main__` block does too, so you can press Run to try your API.

## Example

```python
client = TestClient(app)
client.post("/notes", json={"title": "Groceries"})   # 201 {'id': 1, 'title': 'Groceries', 'body': ''}
client.get("/notes/1")                                # 200 {'id': 1, 'title': 'Groceries', 'body': ''}
client.post("/notes", json={"title": ""})            # 422
client.get("/notes/999")                              # 404 {'detail': 'Note not found'}
```
