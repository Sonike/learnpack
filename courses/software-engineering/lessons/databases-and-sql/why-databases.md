# Why databases

## Why this matters

Almost every program you will be paid to work on stores data: users, orders, messages, invoices. In the early sections you saved data in JSON files, and that works until two people use the program at once, or you need "every order over ₦50,000 from last March", or a bug writes half a record and crashes. A database solves those three problems, and **SQL** is the language you use to talk to it. Every backend job ad lists it, and interviewers often ask you to write a query on the spot.

## 1. The problem with "just a JSON file"

Here is a tiny bookshop program that keeps its data in a file:

```python
import json

with open("books.json") as f:
    books = json.load(f)          # read the WHOLE file into memory

books.append({"title": "Things Fall Apart", "author": "Chinua Achebe", "year": 1958})

with open("books.json", "w") as f:
    json.dump(books, f)           # write the WHOLE file back
```

It looks fine. Now picture what goes wrong as the program grows:

- **Two users at once (concurrency).** Ada and Tunde both load the file, both add a book, both save. Whoever saves last wins, and the other book silently disappears.
- **Asking questions (querying).** To find "books published before 1970 by authors whose name starts with C", you must load every record and loop over them in Python. With 10 million rows, that's slow and eats memory.
- **Keeping data correct (integrity).** Nothing stops a bug from saving `{"title": "", "year": -5}`. Nothing stops a crash halfway through `json.dump` from leaving a broken file.

A **database** is a program whose whole job is to store data safely and answer questions about it quickly. It handles many users at once, only reads the parts it needs, and refuses data that breaks the rules you set.

> **Note:** a JSON file is still fine for small things that one program reads and writes, like a settings file or a list of 20 high scores. Reach for a database when you have many records, many users, or data you can't afford to lose.

## 2. Tables, rows and columns

The most common kind of database is a **relational database**. It stores data in **tables**, which look a lot like spreadsheets:

```
books
+----+-------------------+---------------+------+
| id | title             | author        | year |
+----+-------------------+---------------+------+
|  1 | Things Fall Apart | Chinua Achebe | 1958 |
|  2 | Half of a Yellow  | Chimamanda    | 2006 |
|    |   Sun             |   Adichie     |      |
|  3 | Purple Hibiscus   | Chimamanda    | 2003 |
|    |                   |   Adichie     |      |
+----+-------------------+---------------+------+
```

- A **table** holds one kind of thing: books, users, orders.
- A **column** is one property of that thing, and it has a **type**: `id` is a whole number, `title` is text.
- A **row** is one thing: one book.

The design of your tables (their names, columns, types and rules) is called the **schema**. You write the schema once, and the database enforces it on every write.

## 3. SQL: the language of databases

**SQL** (Structured Query Language, said "S-Q-L" or "sequel") is how you create tables, put data in and ask questions. It reads almost like English. Here is the schema for the table above:

```sql
CREATE TABLE books (
    id     INTEGER PRIMARY KEY,
    title  TEXT NOT NULL,
    author TEXT NOT NULL,
    year   INTEGER
);
```

And here is how you add a row and read it back:

```sql
INSERT INTO books (title, author, year) VALUES ('Things Fall Apart', 'Chinua Achebe', 1958);

SELECT title, year FROM books WHERE year < 1970;
-- Things Fall Apart | 1958
```

A few habits to notice:

- SQL keywords (`CREATE`, `SELECT`) are written in capitals by convention. The database doesn't care; it just makes queries easier to read.
- Text values use **single quotes**: `'Chinua Achebe'`. Double quotes mean something else in SQL (a column or table name).
- `--` starts a comment, like `#` in Python.
- Each statement ends with `;`.

## 4. Primary keys

Two books can share a title, and authors write many books. So how do you point at exactly one row? With a **primary key**: a column whose value is **unique** and **never empty** for every row. Here that's `id`.

```sql
INSERT INTO books (id, title, author) VALUES (1, 'Arrow of God', 'Chinua Achebe');
-- Error: UNIQUE constraint failed: books.id
```

In SQLite, a column declared `INTEGER PRIMARY KEY` fills itself in: if you leave `id` out of an `INSERT`, the database picks the next free number. That's why the earlier `INSERT` didn't mention `id`.

Primary keys matter because other tables will point to rows by their key ("this loan is for book 3"). If keys could repeat or change, those pointers would break. You'll use this in *Relationships and joins*.

## 5. Constraints: rules the database enforces

A **constraint** is a rule on a column. If an `INSERT` or `UPDATE` breaks it, the database refuses the whole statement. The four you'll use most:

| Constraint | Meaning | Example |
|---|---|---|
| `PRIMARY KEY` | unique and identifies the row | `id INTEGER PRIMARY KEY` |
| `NOT NULL` | a value is required | `title TEXT NOT NULL` |
| `UNIQUE` | no two rows may share this value | `isbn TEXT UNIQUE` |
| `CHECK (...)` | a condition that must be true | `pages INTEGER CHECK (pages > 0)` |

**`NULL`** is SQL's word for "no value", like `None` in Python. `NOT NULL` forbids it.

Why put rules in the database instead of only in Python? Because every program that touches the data, today's and next year's, gets the same rules for free, and a bug in one of them can't sneak bad data in. Validating in Python as well is good (it gives friendlier messages), but the database is the last line of defence.

## 6. SQLite and PostgreSQL

There are many relational databases. Two matter for you now:

- **SQLite** is a database in a single file (or in memory). There's no server to install; Python ships with it. Phones, browsers and many desktop apps use it. It's perfect for learning, tests, and small apps.
- **PostgreSQL** ("Postgres") runs as a separate server that many programs connect to over the network. It's the most common choice for web backends.

The good news: the SQL is almost identical. Everything in this section works in both, with small differences that the docs point out. Learn on SQLite, and you can use Postgres at work.

## 7. SQLite from the terminal

If the `sqlite3` command is installed (it is on macOS and most Linux systems), you can open a database file and type SQL directly:

```bash
sqlite3 shop.db
```

```
SQLite version 3.45.1
sqlite> CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
sqlite> INSERT INTO books (title) VALUES ('Arrow of God');
sqlite> SELECT * FROM books;
1|Arrow of God
sqlite> .tables
books
sqlite> .quit
```

Lines starting with a dot (`.tables`, `.schema`, `.quit`) are commands for the `sqlite3` tool itself, not SQL. `SELECT *` means "all columns". Don't worry if `sqlite3` isn't installed on Windows: the Python module below is all you need for this section.

## 8. SQLite from Python

Python's standard library includes the `sqlite3` module. Three steps: **connect**, **execute** SQL, **fetch** results.

```python
import sqlite3

conn = sqlite3.connect(":memory:")      # a throwaway database in RAM
conn.execute("""
    CREATE TABLE books (
        id     INTEGER PRIMARY KEY,
        title  TEXT NOT NULL,
        year   INTEGER CHECK (year > 0)
    )
""")
conn.execute("INSERT INTO books (title, year) VALUES ('Arrow of God', 1964)")
conn.execute("INSERT INTO books (title, year) VALUES ('Anthills of the Savannah', 1987)")

rows = conn.execute("SELECT id, title, year FROM books").fetchall()
print(rows)
# [(1, 'Arrow of God', 1964), (2, 'Anthills of the Savannah', 1987)]
```

- `sqlite3.connect("shop.db")` opens (or creates) a file. `":memory:"` makes a database that disappears when the program ends, which is perfect for experiments and tests.
- `conn.execute(sql)` runs one statement.
- `.fetchall()` returns every result row as a list of tuples. `.fetchone()` returns just the next row, or `None`.

Now watch a constraint protect you:

```python
try:
    conn.execute("INSERT INTO books (title, year) VALUES (NULL, 2001)")
except sqlite3.IntegrityError as e:
    print("Refused:", e)
# Refused: NOT NULL constraint failed: books.title

try:
    conn.execute("INSERT INTO books (title, year) VALUES ('Time Travel', -50)")
except sqlite3.IntegrityError as e:
    print("Refused:", e)
# Refused: CHECK constraint failed: year > 0
```

`sqlite3.IntegrityError` is the exception for "this data breaks a rule". The message tells you exactly which rule.

> **Try it:** in the practice editor, create a table with a `UNIQUE` email column, insert the same email twice, and read the error message.

One more thing: when you write to a **file** database, you must call `conn.commit()` to save the changes. Until then, other programs can't see them, and if your program crashes they're thrown away. You'll learn why (transactions) in *Changing data, schema design and indexes*.

```python
conn = sqlite3.connect("shop.db")
conn.execute("INSERT INTO books (title, year) VALUES ('Arrow of God', 1964)")
conn.commit()      # now it's saved on disk
conn.close()
```

## Common mistakes

**Double quotes around text.**

```sql
INSERT INTO books (title) VALUES ("Arrow of God");
```

SQLite often lets this slide, but in PostgreSQL and in strict SQL it means "the column named Arrow of God", and you get `column "Arrow of God" does not exist`. Use single quotes for text.

**Forgetting `NOT NULL`.** A column without it happily accepts `NULL`. If a book must have a title, say so in the schema, or one day you'll find a row with no title and no idea how it got there.

**Reading `table books already exists`.** Running `CREATE TABLE` twice on the same file fails. Use `CREATE TABLE IF NOT EXISTS books (...)` in scripts that may run more than once.

**Forgetting `commit()`.** Your script runs, prints the new row, and then the row is gone next time. That's a missing `conn.commit()` on a file database.

**Writing `CHECK` with Python syntax.** `CHECK (pages > 0 and pages < 5000)` works because SQL also has `AND` (case doesn't matter), but `CHECK (pages != None)` does not: in SQL you write `pages IS NOT NULL`, or just use `NOT NULL`.

## Using AI here

Asking an AI assistant "why does my CHECK constraint fail?" or "what's the difference between UNIQUE and PRIMARY KEY?" is a good use of it. Write the schema yourself, though: deciding which rules your data needs is the skill, and it's exactly what you'll be asked to explain about your projects.

## Recap

- A database stores data safely for many users, answers questions fast, and enforces rules. JSON files don't.
- Relational databases store **tables** of **rows** and typed **columns**; the design is the **schema**.
- A **primary key** uniquely identifies each row.
- **Constraints** (`NOT NULL`, `UNIQUE`, `CHECK`, `PRIMARY KEY`) make the database refuse bad data; in Python that shows up as `sqlite3.IntegrityError`.
- SQLite (a file, built into Python) and PostgreSQL (a server) speak almost the same SQL.
- In Python: `connect`, `execute`, `fetchall`, and `commit` for file databases.
