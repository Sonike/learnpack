# Building an API with FastAPI

## Why this matters

You built routing, JSON parsing and status codes by hand in *A backend from scratch*. That taught you how it works; it's not how you'd ship. **FastAPI** is a popular Python web framework that does all that plumbing for you, plus validation, error responses and interactive documentation, driven by the type hints you already know. It's widely used in job ads for Python backend roles, and because it builds on standard Python types, what you learn here transfers to other frameworks too.

## 1. Your first FastAPI app

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, world"}
```

That's a complete API. Line by line:

- `app = FastAPI()` creates the application, the same role as your WSGI `app` function.
- `@app.get("/hello")` is a **decorator** that registers a route: `GET` requests for `/hello` go to the function below. FastAPI calls these **path operations**. There's one decorator per method: `@app.post`, `@app.put`, `@app.patch`, `@app.delete`.
- The function returns a dict, and FastAPI turns it into a JSON response with status 200 and the right `Content-Type`.

To run it on your own machine, install FastAPI with its standard extras and start the development server:

```bash
pip install "fastapi[standard]"
fastapi dev main.py
```

```
   FastAPI   Starting development server 🚀
             Serving at: http://127.0.0.1:8000
             API docs: http://127.0.0.1:8000/docs
```

`fastapi dev` uses **Uvicorn**, an ASGI server, and restarts automatically when you save a file. Visit `http://127.0.0.1:8000/hello` and you'll see the JSON. You can also run Uvicorn directly with `uvicorn main:app --reload` ("the `app` object in `main.py`").

> **Note:** the practice editor can't start servers. Exercises use FastAPI's `TestClient` instead (section 7), which calls your app directly, just like you called your WSGI app in the last lesson.

## 2. Path parameters, with types

Path parameters use the same `{name}` pattern you implemented yourself. The difference: give the function parameter a type hint, and FastAPI converts and checks it:

```python
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"id": note_id, "type": str(type(note_id))}
```

```
GET /notes/7    -> 200  {"id": 7, "type": "<class 'int'>"}
GET /notes/abc  -> 422  {"detail": [{"type": "int_parsing",
                          "loc": ["path", "note_id"],
                          "msg": "Input should be a valid integer, unable to parse string as an integer", ...}]}
```

`"7"` arrives as text and your function receives the integer `7`. For `"abc"`, your function never runs; FastAPI answers **422 Unprocessable Content** with a description of exactly what was wrong and where (`loc`). That's the `ValueError` handling you'd otherwise write in every handler.

## 3. Query parameters

Any function parameter that **isn't** in the path is read from the query string. A default value makes it optional:

```python
@app.get("/notes")
def list_notes(limit: int = 10, tag: str | None = None):
    return {"limit": limit, "tag": tag}
```

```
GET /notes                    -> {"limit": 10, "tag": null}
GET /notes?limit=3&tag=work   -> {"limit": 3, "tag": "work"}
GET /notes?limit=lots         -> 422
```

## 4. Request bodies with Pydantic models

To accept JSON in a request body, describe its shape with a **Pydantic model**: a class that inherits from `BaseModel` and lists fields with type hints. Pydantic is the validation library FastAPI is built on.

```python
from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = ""


@app.post("/notes", status_code=201)
def create_note(note: NoteIn):
    return {"id": 1, "title": note.title, "body": note.body}
```

When a parameter's type is a Pydantic model, FastAPI reads the request body as JSON, checks it against the model, and hands you a `NoteIn` object. `Field(min_length=1, max_length=100)` adds rules beyond the type. Send something wrong and you get a 422 that says why:

```
POST /notes {"title": "Groceries"}            -> 201 {"id": 1, "title": "Groceries", "body": ""}
POST /notes {"title": ""}                     -> 422 "String should have at least 1 character"
POST /notes {"body": "no title"}              -> 422 "Field required"
POST /notes {"title": 42}                     -> 422 "Input should be a valid string"
```

This is **validation at the boundary**: bad data is stopped at the edge of your system, before your code or your database ever see it. `status_code=201` on the decorator sets the success status, because `POST` that creates something should answer **201 Created**.

## 5. Response models and errors

You'll often store more than you want to return (a password hash, an internal flag). A **response model** declares exactly what goes out:

```python
class NoteOut(BaseModel):
    id: int
    title: str
    body: str


NOTES = {1: {"id": 1, "title": "Groceries", "body": "", "internal_flag": True}}


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int):
    note = NOTES.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
```

- `response_model=NoteOut` filters and validates the output: extra keys like `internal_flag` are dropped, so `GET /notes/1` returns only `id`, `title` and `body`. (You can also write the return type, `-> NoteOut`, and FastAPI uses that.)
- `raise HTTPException(status_code=404, detail=...)` stops the handler and sends that status with `{"detail": "Note not found"}`. Import it with `from fastapi import FastAPI, HTTPException`.

For a successful `DELETE` with nothing to say, use `status_code=204` and return `None`; a 204 response must have an empty body.

## 6. Dependency injection

Your handlers need a repository (from *SQL from Python, safely*). You could import a global one, but then tests can't swap it for a fake. FastAPI's answer is **dependencies**: a function that provides something, declared with `Depends`:

```python
from fastapi import Depends


class NoteRepository:
    def __init__(self):
        self.notes: dict[int, dict] = {}
        self.next_id = 1

    def add(self, title: str, body: str) -> dict:
        note = {"id": self.next_id, "title": title, "body": body}
        self.notes[note["id"]] = note
        self.next_id += 1
        return note

    def get(self, note_id: int) -> dict | None:
        return self.notes.get(note_id)


repo = NoteRepository()


def get_repo() -> NoteRepository:
    return repo


@app.post("/notes", status_code=201, response_model=NoteOut)
def create_note(note: NoteIn, repo: NoteRepository = Depends(get_repo)):
    return repo.add(note.title, note.body)
```

For each request, FastAPI calls `get_repo()` and passes the result in as `repo`. The handler doesn't know or care where the repository came from. In a real app, `get_repo` might open a database connection; in tests, you replace it.

This is the "handler → repository" layering from the last lesson, with the framework wiring the layers together.

## 7. Testing with TestClient

`TestClient` sends requests to your app **without a server**, and gives back response objects:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

response = client.post("/notes", json={"title": "Groceries"})
print(response.status_code, response.json())
# 201 {'id': 1, 'title': 'Groceries', 'body': ''}

response = client.get("/notes/999")
print(response.status_code, response.json())
# 404 {'detail': 'Note not found'}

response = client.post("/notes", json={"title": ""})
print(response.status_code)
# 422
```

`json=` encodes the dict as the body and sets `Content-Type: application/json` for you. `response.json()` decodes the body.

### Swapping dependencies in tests

`app.dependency_overrides` is a dict: "whenever a handler depends on *this* function, call *that* one instead." Tests use it to hand the app a fresh or fake repository:

```python
class FakeRepo:
    def __init__(self):
        self.added = []

    def add(self, title, body):
        self.added.append(title)
        return {"id": 42, "title": title, "body": body}


fake = FakeRepo()
app.dependency_overrides[get_repo] = lambda: fake
client = TestClient(app)

response = client.post("/notes", json={"title": "Test"})
print(response.json(), fake.added)
# {'id': 42, 'title': 'Test', 'body': ''} ['Test']

app.dependency_overrides.clear()     # put the real one back
```

The fake records what the handler asked it to do, so the test can check that the handler called the repository correctly, with no database at all. This is the dependency injection idea from *Testing and test-driven development*, built into the framework.

## 8. Free interactive docs

Open `http://127.0.0.1:8000/docs` while your app is running. FastAPI generates an interactive page listing every endpoint, its parameters, its body model and its responses, all from your type hints, and lets you send real requests from the browser. The raw description lives at `/openapi.json`, in a standard format called **OpenAPI** that other tools can use to generate client code. Your teammates and future self will thank you: the docs can't drift out of date, because they *are* the code.

## 9. `def` or `async def`?

FastAPI examples often use `async def`. Both work:

- Use plain **`def`** when your handler calls ordinary blocking code, like `sqlite3`. FastAPI runs it in a way that doesn't block other requests.
- Use **`async def`** only when everything inside is async too (using `await` with async libraries).

If you're not sure, use `def`. Calling slow blocking code inside an `async def` handler freezes the whole server while it runs, which is a classic performance bug.

## Common mistakes

**Returning `None` from a GET for a missing item.** You get `200` with `null`, not a 404. `raise HTTPException(status_code=404, ...)` instead.

**Expecting 400 for invalid input.** FastAPI uses **422** for validation errors. That's normal; clients and tests should expect it.

**Putting the body in the URL.** A parameter with a simple type (`title: str`) is read from the **query string**, not the body. If you want it in the JSON body, use a Pydantic model.

**Forgetting `status_code=201` on create.** The default is 200. It still "works", but clients that check for 201 will be confused, and reviewers will notice.

**Not clearing `dependency_overrides`.** Overrides stay on the `app` object. If one test sets an override and doesn't clear it, later tests silently use the fake.

**Reading the error.** A 422's body is a list under `"detail"`. Each item's `loc` says where the problem is (`["body", "title"]`) and `msg` says what. Print `response.json()` in a failing test before guessing.

## Recap

- `@app.get("/path")` and friends register **path operations**; return dicts or models and FastAPI sends JSON.
- Typed **path** and **query** parameters are converted and validated automatically; failures give **422**.
- **Pydantic models** describe request bodies (and `Field(...)` adds rules); **response models** control what goes out.
- `raise HTTPException(status_code=404)` for errors; set `status_code=201`/`204` on the decorator.
- **`Depends`** injects things like repositories; `app.dependency_overrides` swaps them in tests.
- **`TestClient`** tests the app without a server; `/docs` gives free interactive documentation.
