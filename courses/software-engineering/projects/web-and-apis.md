# A REST API with FastAPI

Build a real backend service, in its own GitHub repository: a FastAPI API for something you care about, with a SQLite database, user accounts, and tests for every endpoint. This is the project you'll deploy later in the course, and the one interviewers can poke at live: "show me what happens if I edit someone else's recipe".

## Pick a resource

Choose something with a clear owner per item, so access control matters:

- **Habits:** users track daily habits and check-ins.
- **Recipes:** users publish recipes; anyone can read, only the author can edit.
- **Book club:** users log books and reviews.

Avoid to-do lists, which every reviewer has seen a hundred times. The rest of this brief uses recipes as the example.

## Requirements

### 1. Endpoints

At least six, following REST conventions from *Consuming APIs*:

```
POST   /users                 sign up                      201 / 409 if the email exists
POST   /login                 get a token                  200 / 401
GET    /recipes               list (with ?limit and ?offset or a cursor)   200
POST   /recipes               create (logged in)           201 / 401 / 422
GET    /recipes/{id}          read one                     200 / 404
PATCH  /recipes/{id}          update (owner only)          200 / 401 / 403 / 404 / 422
DELETE /recipes/{id}          delete (owner only)          204 / 401 / 403 / 404
```

### 2. Validation and status codes

- Pydantic models for every request body and response (`RecipeIn`, `RecipeOut`, `UserIn`…). Response models must never include password hashes.
- Use `Field(...)` for real rules: title length, positive cooking time, a valid email shape.
- Return the right codes: 201 for creates, 204 for deletes, 404 for missing items, 409 for duplicates, 401/403 for auth problems.

### 3. SQLite through a repository

- Reuse what you built in *Databases and SQL*: a schema with foreign keys and constraints, and a repository class with parameterised queries only.
- Inject it with `Depends(get_repo)`. Tests override `get_repo` with a repository on a fresh `:memory:` database (create the connection with `check_same_thread=False`, because FastAPI may run handlers on a different thread from the one that created it).
- No ORM. You'll appreciate ORMs more after this.

### 4. Authentication and authorisation

- Hash passwords with a library: `argon2-cffi` (recommended) or `bcrypt`. Never store or log a plain password.
- On login, return a signed token with an expiry, like the one you built in *Auth and security basics* (or use the `PyJWT` library). Read the signing secret from an environment variable.
- Clients send `Authorization: Bearer <token>`. Write a `current_user` dependency that verifies the token and raises 401 if it's missing, invalid or expired.
- Authorisation lives in one function like `can_edit(user, recipe)`. A test proves user A **cannot** edit or delete user B's recipe.

### 5. Tests

- `TestClient` tests for **every** endpoint, including the error paths: 401 without a token, 403 for someone else's item, 404, 409, 422.
- Each test starts from an empty database (a fixture or helper that sets `app.dependency_overrides`, and clears it afterwards).
- Run them with `pytest`; they should take a few seconds at most.

### 6. Docs

- FastAPI's `/docs` page works, and your endpoints have short docstrings, which appear there.
- The README explains how to install, set the environment variables, run (`fastapi dev`), and test, with one example `curl` request and its response.

## Suggested order

1. The recipes endpoints with an in-memory repository and tests, no auth.
2. Swap in the SQLite repository; the tests shouldn't need to change much.
3. Users, password hashing and login.
4. The `current_user` dependency, then ownership checks, test first.
5. README and tidy-up.

## Using AI on this project

Use an AI assistant to explain FastAPI errors, review your access-control logic, or suggest missing test cases. Write the handlers, queries and tests yourself. In an interview you'll be asked why a request returns 403 rather than 404, and you need to know because you decided it.

## Stretch goals

- Pagination with cursors, and a test that walks every page.
- Rate-limit `/login` (for example, 5 failed attempts per email per 15 minutes, with time injected so it's testable).
- An `updated_at` column and a 409 when a client updates a recipe that changed since they read it.
