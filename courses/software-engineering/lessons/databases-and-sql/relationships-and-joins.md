# Relationships and joins

## Why this matters

Real data is connected. An author writes many books; a member borrows many books, and a book is borrowed by many members over time. If you cram all of that into one table, you repeat the same facts over and over and they drift out of sync. Relational databases solve this by keeping each kind of thing in its own table and linking the tables with keys. **Joins** are how you put the pieces back together when you ask a question. "Show each loan with the member's name and the book's title" is a join, and you'll write one in almost every backend feature.

## 1. Why split data into several tables

Imagine a library that stores loans in a single table:

```
loans (one big table)
+-------------------+---------------+------------------------+--------+
| book_title        | author_name   | author_country         | member |
+-------------------+---------------+------------------------+--------+
| Things Fall Apart | Chinua Achebe | Nigeria                | Ada    |
| Things Fall Apart | Chinua Achebe | Nigeria                | Tunde  |
| Purple Hibiscus   | C. N. Adichie | Nigeria                | Tunde  |
+-------------------+---------------+------------------------+--------+
```

Achebe's name and country are stored twice. If someone fixes a typo in one row and not the other, the data now disagrees with itself. And where do you store an author who has no books in the library yet? There's no loan row to put them in.

The fix is one table per kind of thing, linked by ids:

```
authors                 books                              members
+----+---------------+  +----+-------------------+-----------+  +----+-------+
| id | name          |  | id | title             | author_id |  | id | name  |
+----+---------------+  +----+-------------------+-----------+  +----+-------+
|  1 | Chinua Achebe |  |  1 | Things Fall Apart |         1 |  |  1 | Ada   |
|  2 | C. N. Adichie |  |  2 | Arrow of God      |         1 |  |  2 | Tunde |
|  3 | Wole Soyinka  |  |  3 | Purple Hibiscus   |         2 |  +----+-------+
+----+---------------+  |  4 | Americanah        |         2 |
                        +----+-------------------+-----------+
loans
+----+---------+-----------+------------+------------+-------------+
| id | book_id | member_id | loaned_on  | due_on     | returned_on |
+----+---------+-----------+------------+------------+-------------+
|  1 |       1 |         1 | 2026-01-10 | 2026-01-24 | 2026-01-20  |
|  2 |       3 |         2 | 2026-02-01 | 2026-02-15 | NULL        |
|  3 |       1 |         2 | 2026-02-03 | 2026-02-17 | NULL        |
+----+---------+-----------+------------+------------+-------------+
```

Each fact now lives in exactly one place. Wole Soyinka exists even with no books.

## 2. One-to-many and many-to-many

There are two shapes of relationship you'll meet constantly.

**One-to-many:** one author has many books, but each book has one author. The link goes on the **"many" side**: each book row stores its `author_id`. (You can't put a list of book ids in an author row; a column holds one value.)

```
authors 1 ─────< many books        (books.author_id points at authors.id)
```

**Many-to-many:** a member borrows many books, and a book is borrowed by many members. Neither side can hold a single id, so you add a third table in between, called a **join table**, where each row links one of each. Here that's `loans`, which also carries its own facts (the dates).

```
members 1 ───< loans >─── 1 books
```

## 3. Foreign keys

A column like `books.author_id` that points at another table's primary key is called a **foreign key**. You declare it with `REFERENCES`:

```sql
CREATE TABLE authors (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE books (
    id        INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id)
);
```

With the foreign key in place, the database refuses links to things that don't exist, and refuses to delete things that are still linked:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")   # SQLite: switch enforcement on!
conn.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn.execute("""CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL,
                author_id INTEGER NOT NULL REFERENCES authors(id))""")
conn.execute("INSERT INTO authors (id, name) VALUES (1, 'Chinua Achebe')")
conn.execute("INSERT INTO books (title, author_id) VALUES ('Arrow of God', 1)")   # fine

try:
    conn.execute("INSERT INTO books (title, author_id) VALUES ('Ghost Book', 99)")
except sqlite3.IntegrityError as e:
    print(e)
# FOREIGN KEY constraint failed

try:
    conn.execute("DELETE FROM authors WHERE id = 1")
except sqlite3.IntegrityError as e:
    print(e)
# FOREIGN KEY constraint failed
```

> **Note:** for historical reasons, SQLite does **not** enforce foreign keys unless you run `PRAGMA foreign_keys = ON` on every new connection. Without it, both statements above succeed silently and you get "orphan" books pointing at nobody. PostgreSQL always enforces them. A `PRAGMA` is a SQLite-specific setting command.

## 4. INNER JOIN: rows that match on both sides

A **join** combines rows from two tables using a condition, usually "this foreign key equals that primary key":

```sql
SELECT books.title, authors.name
FROM books
JOIN authors ON books.author_id = authors.id;
-- ('Things Fall Apart', 'Chinua Achebe')
-- ('Arrow of God', 'Chinua Achebe')
-- ('Purple Hibiscus', 'C. N. Adichie')
-- ('Americanah', 'C. N. Adichie')
```

Read it as: "for every book, find the author whose `id` equals the book's `author_id`, and give me one combined row." `JOIN` is short for `INNER JOIN`. It keeps only pairs that match, so Wole Soyinka (no books) doesn't appear.

Typing table names gets long, so give each table a short alias:

```sql
SELECT b.title, a.name
FROM books AS b
JOIN authors AS a ON b.author_id = a.id
WHERE a.name LIKE '%Achebe%';
-- ('Things Fall Apart', 'Chinua Achebe')
-- ('Arrow of God', 'Chinua Achebe')
```

You can chain joins. Each loan with the member's name and the book's title:

```sql
SELECT m.name, b.title, l.due_on
FROM loans AS l
JOIN members AS m ON l.member_id = m.id
JOIN books   AS b ON l.book_id   = b.id
ORDER BY l.id;
-- ('Ada', 'Things Fall Apart', '2026-01-24')
-- ('Tunde', 'Purple Hibiscus', '2026-02-15')
-- ('Tunde', 'Things Fall Apart', '2026-02-17')
```

## 5. LEFT JOIN: keep everything on the left

A `LEFT JOIN` keeps **every** row from the left table (the one after `FROM`), matched or not. When there's no match, the right side's columns are filled with `NULL`:

```sql
SELECT a.name, b.title
FROM authors AS a
LEFT JOIN books AS b ON b.author_id = a.id
ORDER BY a.id, b.id;
-- ('Chinua Achebe', 'Things Fall Apart')
-- ('Chinua Achebe', 'Arrow of God')
-- ('C. N. Adichie', 'Purple Hibiscus')
-- ('C. N. Adichie', 'Americanah')
-- ('Wole Soyinka', None)
```

Five rows instead of four. Here's the difference side by side:

```
INNER JOIN  ->  only matched pairs                    (4 rows)
LEFT JOIN   ->  matched pairs + unmatched left rows   (5 rows, NULLs on the right)
```

## 6. Finding rows with no match

That `NULL` is the key to a question you'll ask all the time: "which X have no Y?" Left-join, then keep only the rows where the right side is missing:

```sql
-- Books that have never been borrowed
SELECT b.title
FROM books AS b
LEFT JOIN loans AS l ON l.book_id = b.id
WHERE l.id IS NULL
ORDER BY b.title;
-- ('Americanah',)
-- ('Arrow of God',)
```

Test the right table's **primary key** (`l.id`) for `NULL`. It can only be `NULL` when there was no match, so the test is reliable.

## 7. Joins with GROUP BY

Joins and grouping combine naturally. Loans per author, including authors with none:

```sql
SELECT a.name, COUNT(l.id) AS loan_count
FROM authors AS a
LEFT JOIN books AS b ON b.author_id = a.id
LEFT JOIN loans AS l ON l.book_id = b.id
GROUP BY a.id
ORDER BY loan_count DESC, a.name;
-- ('Chinua Achebe', 2)
-- ('C. N. Adichie', 1)
-- ('Wole Soyinka', 0)
```

Two details make this right. `LEFT JOIN` keeps Soyinka in the result. And `COUNT(l.id)` counts only non-`NULL` loan ids, so he gets 0. `COUNT(*)` would count his one all-`NULL` row and wrongly give him 1. We group by `a.id` rather than `a.name` so two authors who happen to share a name stay separate.

## 8. Dates as text

SQLite has no separate date type. The common convention is to store dates as ISO 8601 text, `'YYYY-MM-DD'`. Because the biggest unit comes first, these strings sort and compare in date order:

```sql
-- Loans not returned and past their due date, as of 1 March 2026
SELECT m.name, l.due_on
FROM loans AS l
JOIN members AS m ON l.member_id = m.id
WHERE l.returned_on IS NULL AND l.due_on < '2026-03-01';
-- ('Tunde', '2026-02-15')
-- ('Tunde', '2026-02-17')
```

Tunde appears twice because he has two overdue loans. Add `DISTINCT` (`SELECT DISTINCT m.name ...`) to get each name once. In real code, "today" shouldn't be typed into the query; you'll pass it in as a parameter (a `?` placeholder), which the practice exercise uses.

## 9. Subqueries

A **subquery** is a query inside another query, in brackets. It's sometimes easier to read than a join:

```sql
SELECT title FROM books
WHERE id NOT IN (SELECT book_id FROM loans)
ORDER BY title;
-- ('Americanah',)
-- ('Arrow of God',)
```

The inner query produces a list of borrowed book ids; the outer one keeps books not in that list. Same answer as the `LEFT JOIN ... IS NULL` version. Use whichever reads more clearly to you. One trap: if the subquery's list contains a `NULL`, `NOT IN` returns no rows at all (the "unknown" logic from *Querying with SELECT* again), so prefer the `LEFT JOIN` form when the column can be `NULL`.

## Common mistakes

**Forgetting the `ON` condition, or getting it wrong.** `SELECT * FROM books JOIN authors` with no `ON` pairs every book with every author: 4 × 3 = 12 rows. If your result suddenly has far too many rows, check the join condition.

**`ambiguous column name: id`.** Both tables have an `id`, and SQLite can't guess which you mean. Prefix it: `b.id` or `a.id`.

**Filtering the right table in `WHERE` after a `LEFT JOIN`.** In `books AS b LEFT JOIN loans AS l ON l.book_id = b.id WHERE l.member_id = 2`, the unmatched books have `NULL` in `l.member_id`, so the `WHERE` drops them and your `LEFT JOIN` quietly behaves like an inner one. To keep unmatched rows, put the condition in the `ON` clause: `ON l.book_id = b.id AND l.member_id = 2`.

**Foreign keys "not working" in SQLite.** You forgot `PRAGMA foreign_keys = ON` on this connection.

**`COUNT(*)` with a `LEFT JOIN`.** It counts the unmatched row as 1. Count a column from the right table instead.

## Recap

- Keep each kind of thing in its own table and link them with ids; each fact lives in one place.
- One-to-many: the **foreign key** goes on the "many" side. Many-to-many: add a **join table**.
- `REFERENCES` makes the database reject broken links; SQLite needs `PRAGMA foreign_keys = ON`.
- `JOIN` (inner) keeps matched pairs; `LEFT JOIN` keeps every left row and fills gaps with `NULL`.
- "Which X have no Y?" is `LEFT JOIN ... WHERE right.id IS NULL`.
- Store dates as `'YYYY-MM-DD'` text so they compare correctly; subqueries are queries inside brackets.
