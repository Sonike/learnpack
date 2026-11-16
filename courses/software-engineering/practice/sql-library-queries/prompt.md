# Library reports with joins

A small library keeps its data in four linked tables. Write three reports as **SQL strings** (constants in `solution.py`). The tests run them against sample data and compare rows exactly.

```
authors(id, name)
books(id, title, author_id -> authors.id)
members(id, name)
loans(id, book_id -> books.id, member_id -> members.id, loaned_on, due_on, returned_on)
```

Dates are ISO text like `'2026-02-15'`. `returned_on` is `NULL` while a book is still out. The starter's `make_db()` builds the sample data so you can try your queries.

| Constant | Question | Columns | Row order |
|---|---|---|---|
| `NEVER_BORROWED` | Books that have never been borrowed | `title` | A→Z |
| `LOANS_PER_AUTHOR` | Number of loans of each author's books, **including authors with 0** (some have no books at all) | `name`, `loan_count` | count high→low, ties by name A→Z |
| `OVERDUE_MEMBERS` | Members with at least one loan that is not returned and whose `due_on` is **before** today. Each name once. | `name` | A→Z |

`OVERDUE_MEMBERS` uses **one `?` placeholder** for today's date; the tests run it like this:

```python
conn.execute(OVERDUE_MEMBERS, ("2026-03-01",)).fetchall()
```

A loan due *on* today isn't overdue yet.

Hints: `LEFT JOIN ... WHERE right_table.id IS NULL`, two `LEFT JOIN`s with `COUNT(loans.id)`, and `SELECT DISTINCT`.

## Example

```python
conn = make_db()
conn.execute(NEVER_BORROWED).fetchall()
# [('Arrow of God',), ('The Joys of Motherhood',)]
```
