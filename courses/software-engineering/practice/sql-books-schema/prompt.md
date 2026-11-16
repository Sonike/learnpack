# Design a books table with rules

Write `create_schema(conn)` that creates a `books` table the database itself keeps clean. Bad rows must be refused with `sqlite3.IntegrityError`, without any checks in Python.

```python
def create_schema(conn: sqlite3.Connection) -> None: ...
```

- `conn` is an open `sqlite3` connection (the tests use `sqlite3.connect(":memory:")`).
- The function creates the table and returns nothing.

The `books` table needs these columns and rules:

| Column | Type | Rules |
|---|---|---|
| `id` | `INTEGER` | primary key (fills itself in when left out) |
| `title` | `TEXT` | required, and not an empty string |
| `author` | `TEXT` | required |
| `year` | `INTEGER` | optional, but if given it must be between 1450 and 2100 |
| `pages` | `INTEGER` | required, and greater than 0 |
| `isbn` | `TEXT` | optional, but no two books may share one |

Hints: `NOT NULL`, `UNIQUE` and `CHECK (...)`. A `CHECK` on an optional column passes when the value is `NULL`, which is what you want for `year`. For "not an empty string", compare with `''`.

## Example

```python
conn = sqlite3.connect(":memory:")
create_schema(conn)
conn.execute("INSERT INTO books (title, author, year, pages, isbn) VALUES ('Arrow of God', 'Chinua Achebe', 1964, 230, '978-0385014809')")  # fine
conn.execute("INSERT INTO books (title, author, pages) VALUES ('Untitled', 'Anon', 0)")
# sqlite3.IntegrityError: CHECK constraint failed: pages > 0
```
