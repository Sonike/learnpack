# Fix the injectable queries

A teammate wrote two lookup functions using f-strings. They work for "Ada", but a user named O'Brien crashes them, and anyone can type `' OR '1'='1` to read the whole table. Rewrite both so every value goes through a `?` parameter.

```python
def find_user(conn: sqlite3.Connection, name: str) -> dict | None: ...
def search_users(conn: sqlite3.Connection, text: str) -> list[str]: ...
```

The `users` table (the starter's `make_db()` creates it): `id`, `name`, `email`.

- **`find_user(conn, name)`**: the user whose name is **exactly** `name`, as `{"id": ..., "name": ..., "email": ...}`, or `None` if there isn't one.
- **`search_users(conn, text)`**: the names that **contain** `text` anywhere (any case), sorted A→Z.

For `search_users`, the `%` wildcards belong in the **value**, not the SQL: write `WHERE name LIKE ?` and pass `(f"%{text}%",)`. Building a value with an f-string is fine; building **SQL** with one is not.

## Example

```python
conn = make_db()
find_user(conn, "O'Brien")        # {'id': 3, 'name': "O'Brien", 'email': 'obrien@example.com'}
find_user(conn, "' OR '1'='1")    # None
search_users(conn, "ad")          # ['Ada', 'Adaeze', 'Chinedu Adamu']
```
