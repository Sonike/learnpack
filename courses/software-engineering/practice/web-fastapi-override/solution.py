from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = ""


class NoteRepository:
    """In-memory storage. A real app might use SQLite here instead."""

    def __init__(self):
        self.notes: dict[int, dict] = {}
        self.next_id = 1

    def add(self, title: str, body: str) -> dict:
        note = {"id": self.next_id, "title": title, "body": body}
        self.notes[self.next_id] = note
        self.next_id += 1
        return note

    def get(self, note_id: int) -> dict | None:
        return self.notes.get(note_id)

    def delete(self, note_id: int) -> bool:
        return self.notes.pop(note_id, None) is not None


repo = NoteRepository()


def get_repo() -> NoteRepository:
    return repo


@app.post("/notes", status_code=201)
def create_note(note: NoteIn, repo: NoteRepository = Depends(get_repo)):
    return repo.add(note.title, note.body)


@app.get("/notes/{note_id}")
def get_note(note_id: int, repo: NoteRepository = Depends(get_repo)):
    note = repo.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, repo: NoteRepository = Depends(get_repo)):
    if not repo.delete(note_id):
        raise HTTPException(status_code=404, detail="Note not found")


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)
    print(client.post("/notes", json={"title": "Hi"}).json())
