from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

NOTES: dict[int, dict] = {}   # note id -> {"id": ..., "title": ..., "body": ...}
next_id = 1


class NoteIn(BaseModel):
    # TODO: title must be 1-100 characters: use Field(min_length=..., max_length=...)
    title: str
    body: str = ""


class Note(BaseModel):
    id: int
    title: str
    body: str


# TODO: POST /notes        -> 201, the new note
# TODO: GET /notes         -> all notes
# TODO: GET /notes/{id}    -> the note, or 404 "Note not found"
# TODO: DELETE /notes/{id} -> 204, or 404 "Note not found"


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)
    for method, url, body in [
        ("POST", "/notes", {"title": "Groceries"}),
        ("GET", "/notes/1", None),
        ("POST", "/notes", {"title": ""}),
        ("GET", "/notes/999", None),
        ("DELETE", "/notes/1", None),
    ]:
        response = client.request(method, url, json=body)
        print(method, url, "->", response.status_code, response.text)
