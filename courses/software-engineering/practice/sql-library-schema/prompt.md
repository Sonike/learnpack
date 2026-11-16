# A library schema with foreign keys

Write `create_library_schema(conn)` that creates four linked tables and makes SQLite **enforce** the links, so the database refuses broken data on its own.

```python
def create_library_schema(conn: sqlite3.Connection) -> None: ...
```

- `conn` is a fresh `sqlite3` connection. Your function must switch foreign-key enforcement on for it (SQLite leaves it off by default), then create the tables.

| Table | Columns |
|---|---|
| `authors` | `id` INTEGER primary key, `name` TEXT required |
| `books` | `id` INTEGER primary key, `title` TEXT required, `author_id` INTEGER required, references `authors(id)` |
| `members` | `id` INTEGER primary key, `name` TEXT required |
| `loans` | `id` INTEGER primary key, `book_id` INTEGER required, references `books(id)`; `member_id` INTEGER required, references `members(id)`; `loaned_on` TEXT required; `due_on` TEXT required; `returned_on` TEXT optional |

After your function runs, these must all raise `sqlite3.IntegrityError`:

- adding a book whose `author_id` doesn't exist, or is `NULL`
- deleting an author who still has books
- adding a loan for a member or book that doesn't exist

…while deleting an author with **no** books still works.

> Watch out: `conn.executescript(...)` is handy for several `CREATE TABLE` statements, but run the `PRAGMA` with `conn.execute(...)` first.

## Example

```python
conn = sqlite3.connect(":memory:")
create_library_schema(conn)
conn.execute("INSERT INTO authors (id, name) VALUES (1, 'Chinua Achebe')")
conn.execute("INSERT INTO books (title, author_id) VALUES ('Arrow of God', 1)")
conn.execute("DELETE FROM authors WHERE id = 1")
# sqlite3.IntegrityError: FOREIGN KEY constraint failed
```
