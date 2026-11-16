# SQL from Python, safely

## Why this matters

Your programs will build SQL using values that come from users: a search box, a login form, a URL. Done the wrong way, a user can type SQL into that box and your database will run it. This is **SQL injection**, and it has leaked millions of passwords and credit card numbers. It's also one of the easiest security bugs to prevent: one habit, used every time. This lesson covers that habit, plus the patterns that keep database code tidy as a program grows: cursors, row factories, transactions, and a **repository layer**.

## 1. Connections and cursors

You've been calling `conn.execute(...)`. Behind the scenes that creates a **cursor**: an object that runs one statement and walks through its results. You can create one explicitly, and you'll see this style in a lot of code:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE)")
cur.execute("INSERT INTO users (name, email) VALUES ('Ada', 'ada@example.com')")
print(cur.lastrowid)   # 1  (the id the database just assigned)

cur.execute("SELECT id, name FROM users")
print(cur.fetchone())  # (1, 'Ada')
print(cur.fetchone())  # None  (no more rows)
```

Useful cursor attributes and methods:

| Name | What it gives you |
|---|---|
| `fetchone()` | the next row, or `None` |
| `fetchall()` | all remaining rows as a list |
| `lastrowid` | the id of the row just inserted |
| `rowcount` | how many rows an `UPDATE`/`DELETE` changed |

`conn.execute(...)` returns the cursor too, so `conn.execute(sql).fetchall()` and the explicit style do the same thing. You can also loop over a cursor directly: `for row in conn.execute(sql): ...`.

## 2. Getting dict-like rows

Tuples are easy to mix up: was it `row[1]` or `row[2]` for the email? Set the connection's **row factory** to `sqlite3.Row` and you can use column names:

```python
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT id, name, email FROM users").fetchone()
print(row["name"], row["email"])   # Ada ada@example.com
print(dict(row))                   # {'id': 1, 'name': 'Ada', 'email': 'ada@example.com'}
```

`sqlite3.Row` still works like a tuple (`row[0]`), so existing code keeps working.

## 3. SQL injection, step by step

Here's a function that looks innocent. It uses an f-string to put the name into the query:

```python
def find_user(conn, name):
    sql = f"SELECT id, name, email FROM users WHERE name = '{name}'"
    return conn.execute(sql).fetchall()

print(find_user(conn, "Ada"))
# [(1, 'Ada', 'ada@example.com')]
```

Now a user types this into the search box instead of a name:

```
' OR '1'='1
```

The f-string pastes it straight into the SQL. The database receives:

```sql
SELECT id, name, email FROM users WHERE name = '' OR '1'='1'
```

`'1'='1'` is true for every row, so the function returns **every user in the table**. The user's input stopped being *data* and became part of the *code*. A nastier input can end the statement and add a new one, or read other tables. And there's a plain bug too: a real user named `O'Brien` crashes the function, because their apostrophe ends the string early:

```
sqlite3.OperationalError: near "Brien": syntax error
```

You might think "I'll escape the quotes myself" or "I'll strip dangerous characters". Don't. People have tried for 25 years and attackers keep finding gaps (other quote characters, encodings, comments). There's a correct solution built into every database library.

## 4. The fix: parameters

Write a `?` placeholder where each value goes, and pass the values separately as a tuple:

```python
def find_user(conn, name):
    sql = "SELECT id, name, email FROM users WHERE name = ?"
    return conn.execute(sql, (name,)).fetchall()

print(find_user(conn, "Ada"))          # [(1, 'Ada', 'ada@example.com')]
print(find_user(conn, "' OR '1'='1"))  # []   (no user has that strange name)
print(find_user(conn, "O'Brien"))      # []   (no crash)
```

Why this is safe: the SQL text and the values travel to the database **separately**. The database parses the SQL first, with the `?` as a hole, and only then drops the value into the hole as plain data. Nothing in the value can ever be read as SQL, no matter what characters it contains.

Two details trip people up:

- The values must be a **sequence**, even for one value: `(name,)` with the trailing comma is a one-item tuple. `(name)` is just `name` in brackets, and a 3-letter string would be treated as 3 separate values.
- Placeholders work for **values only**, not for table or column names. `SELECT * FROM ?` is an error. If a column name must vary (say, a sort column chosen by the user), check it against a fixed list in Python: `if column not in {"name", "email"}: raise ValueError(...)`.

You can also use named placeholders, which read better with many values:

```python
conn.execute(
    "INSERT INTO users (name, email) VALUES (:name, :email)",
    {"name": "Tunde", "email": "tunde@example.com"},
)
```

The rule for the rest of your career: **never build SQL with f-strings, `+`, `%` or `.format()` when any part comes from outside your code.** PostgreSQL libraries use `%s` instead of `?`, but the idea is identical.

## 5. A repository layer

As a program grows, SQL scattered everywhere becomes a problem: the same query is copied into five places, and changing a column means hunting for all of them. A common fix is a **repository**: one class (or module of functions) that owns all the SQL for one kind of thing. The rest of the program calls plain Python methods and never sees SQL.

```python
import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL)"
        )

    def add(self, name: str, email: str) -> User:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)", (name, email)
            )
        return User(cur.lastrowid, name, email)

    def get(self, user_id: int) -> User | None:
        row = self.conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return User(*row) if row else None


repo = UserRepository(sqlite3.connect(":memory:"))
ada = repo.add("Ada", "ada@example.com")
print(ada)              # User(id=1, name='Ada', email='ada@example.com')
print(repo.get(1))      # User(id=1, name='Ada', email='ada@example.com')
print(repo.get(99))     # None
```

What this buys you:

- **One place to look.** Every users query is in one class. Changing the schema means changing one file.
- **Safety by default.** Parameters are used in one place, reviewed once.
- **Plain objects out.** Callers get `User` dataclasses (from *Objects, design and clean code*), not tuples or cursors, so they don't depend on the database at all.
- **Easy tests.** You can test the repository against `:memory:`, and test the rest of the app with a fake repository. You'll lean on this in *A backend from scratch* and *Building an API with FastAPI*.

`User(*row)` unpacks the tuple `(1, 'Ada', 'ada@example.com')` into the three arguments, in column order. That's why the `SELECT` lists the columns in the same order as the dataclass fields.

## 6. Transactions in a repository

Each method that writes should commit its own work, usually with `with self.conn:` as above. If one method does several writes that belong together, put them all inside one `with` block so they succeed or fail as a unit, as you did with the transfer in *Changing data, schema design and indexes*.

## 7. ORMs, and why you're learning SQL first

An **ORM** (Object-Relational Mapper), such as SQLAlchemy or the Django ORM, generates SQL for you from Python classes:

```python
# SQLAlchemy-style, for illustration only
session.query(User).filter(User.name == "Ada").first()
```

ORMs are popular and you'll likely use one at work. They use parameters internally, so they protect you from injection too. But they hide the SQL, and when a page is slow, or a report is wrong, or an interviewer asks for a `GROUP BY`, you need to know what's happening underneath. Engineers who know SQL use ORMs well; engineers who only know the ORM get stuck. Once you're comfortable with this section, picking up an ORM takes days.

## 8. NoSQL, in one paragraph

You'll hear about **NoSQL** databases: document stores like MongoDB (records as JSON-like documents), key-value stores like Redis (a giant, fast dictionary, often used as a cache), and others. They trade some of SQL's guarantees or query power for flexibility or speed in specific situations. Relational databases remain the default for most applications, and the ideas you've learned (keys, indexes, transactions) carry over. Learn them when a job needs them.

## Common mistakes

**`Incorrect number of bindings supplied. The current statement uses 1, and there are 3 supplied.`** You passed `("Ada")` instead of `("Ada",)`. Without the comma, it's a string, and each character became a value.

**`sqlite3.ProgrammingError: Error binding parameter 1: type 'list' is not supported`.** You passed a Python list or dict as a single value. Each `?` takes one simple value: text, number, `None` or bytes.

**Using placeholders for names.** `"ORDER BY ?"` doesn't fail, but it sorts by a constant and so does nothing useful. Validate column names against an allowed list instead.

**"It's only an internal tool."** Internal tools get exposed, copied and reused. Use parameters everywhere; it costs nothing.

**Forgetting `row_factory` was set.** Code that compares a row to a tuple (`row == (1, 'Ada')`) behaves differently with `sqlite3.Row`. Convert with `tuple(row)` or `dict(row)` when you need a plain value.

## Using AI here

AI assistants sometimes produce f-string SQL, especially for "quick" scripts. Treat that as a bug when you review generated code, and tell the assistant to use parameters. Spotting this is a skill reviewers expect from juniors.

## Recap

- A **cursor** runs a statement and hands back rows; `lastrowid` and `rowcount` tell you what changed.
- `conn.row_factory = sqlite3.Row` gives rows you can index by column name.
- **SQL injection** happens when user input is pasted into SQL text; it turns data into code.
- **Always use parameters** (`?` or `:name`) and pass values separately, as a tuple: `(value,)`.
- A **repository** keeps all SQL for one thing in one class and returns plain objects.
- ORMs generate SQL for you; learn SQL first so you can debug what they do.
