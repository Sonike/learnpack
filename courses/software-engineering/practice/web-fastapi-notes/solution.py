from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

NOTES: dict[int, dict] = {}   # note id -> {"id": ..., "title": ..., "body": ...}
next_id = 1


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = ""


class Note(BaseModel):
    id: int
    title: str
    body: str


def find_note(note_id: int) -> dict:
    note = NOTES.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.post("/notes", status_code=201, response_model=Note)
def create_note(note: NoteIn):
    global next_id
    saved = {"id": next_id, "title": note.title, "body": note.body}
    NOTES[next_id] = saved
    next_id += 1
    return saved


@app.get("/notes", response_model=list[Note])
def list_notes():
    return list(NOTES.values())


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    return find_note(note_id)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    find_note(note_id)
    del NOTES[note_id]


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)
    print(client.post("/notes", json={"title": "Groceries"}).json())
