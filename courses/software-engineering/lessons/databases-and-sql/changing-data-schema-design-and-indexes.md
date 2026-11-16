# Changing data, schema design and indexes

## Why this matters

Reading data can't hurt anyone. Changing it can. One `UPDATE` without a `WHERE` sets every customer's balance to zero; a crash halfway through a money transfer takes ₦10,000 from Ada and never gives it to Tunde. This lesson covers the statements that change data, the **transactions** that make a group of changes all-or-nothing, how to design tables that don't contradict themselves, and **indexes**, which turn a query that takes seconds into one that takes microseconds. These are exactly the topics that come up when something goes wrong in production.

## 1. INSERT, UPDATE, DELETE

You've met `INSERT`. Its two partners change and remove existing rows:

```sql
INSERT INTO accounts (owner, balance) VALUES ('Ada', 5000);

UPDATE accounts SET balance = balance + 1000 WHERE owner = 'Ada';

DELETE FROM accounts WHERE owner = 'Ada';
```

- `UPDATE table SET column = value WHERE condition` changes the matching rows. `SET` can use the old value: `balance = balance + 1000`.
- `DELETE FROM table WHERE condition` removes the matching rows.

Now the most important rule in this lesson. **`UPDATE` and `DELETE` without `WHERE` affect every row in the table.**

```sql
UPDATE accounts SET balance = 0;        -- everyone's balance is now 0
DELETE FROM accounts;                   -- the table is now empty
```

There's no "are you sure?". A good habit: write the `WHERE` first, and run it as a `SELECT` to see which rows you're about to change:

```sql
SELECT * FROM accounts WHERE owner = 'Ada';    -- check: 1 row, the right one
UPDATE accounts SET balance = 0 WHERE owner = 'Ada';
```

In Python, `cursor.rowcount` tells you how many rows a change touched, which is a good way to notice "I meant to update one row and updated none":

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER)")
conn.execute("INSERT INTO accounts (owner, balance) VALUES ('Ada', 5000), ('Tunde', 1000)")

cur = conn.execute("UPDATE accounts SET balance = balance + 500 WHERE owner = 'Tunde'")
print(cur.rowcount)   # 1
cur = conn.execute("UPDATE accounts SET balance = balance + 500 WHERE owner = 'Zainab'")
print(cur.rowcount)   # 0  (no such account, and no error!)
```

## 2. Transactions: all or nothing

Moving money is two changes: take from one account, add to another.

```sql
UPDATE accounts SET balance = balance - 2000 WHERE id = 1;
UPDATE accounts SET balance = balance + 2000 WHERE id = 2;
```

If the program crashes between those lines, or the second statement fails, ₦2,000 has vanished. A **transaction** groups statements so they either **all** happen or **none** do. This property is called **atomicity** (from "atom", something that can't be split).

```
BEGIN
  UPDATE ... -2000      ┐
  UPDATE ... +2000      ┘ changes are pending, invisible to others
COMMIT    -> all changes become permanent together
   or
ROLLBACK  -> all pending changes are thrown away, as if nothing happened
```

Atomicity is the "A" in **ACID**, the four guarantees of a reliable database: Atomicity, Consistency (constraints always hold), Isolation (transactions running at the same time don't see each other's half-done work) and Durability (once committed, it survives a crash). You don't need to recite them, but you'll hear the word.

## 3. Transactions in Python

Python's `sqlite3` starts a transaction for you before the first `INSERT`, `UPDATE` or `DELETE`. You end it with `conn.commit()` or `conn.rollback()`. The cleanest way is to use the connection as a **context manager**, with `with`:

```python
with conn:
    conn.execute("UPDATE accounts SET balance = balance - 2000 WHERE id = 1")
    conn.execute("UPDATE accounts SET balance = balance + 2000 WHERE id = 2")
# leaving the block normally   -> conn.commit()
# leaving it with an exception -> conn.rollback(), then the exception continues
```

Let's prove the rollback works. Give the table a `CHECK` so balances can't go negative, then try to overspend:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE accounts (
    id INTEGER PRIMARY KEY, owner TEXT NOT NULL,
    balance INTEGER NOT NULL CHECK (balance >= 0))""")
conn.execute("INSERT INTO accounts (owner, balance) VALUES ('Ada', 5000), ('Tunde', 1000)")
conn.commit()

try:
    with conn:
        conn.execute("UPDATE accounts SET balance = balance + 9000 WHERE id = 2")  # works
        conn.execute("UPDATE accounts SET balance = balance - 9000 WHERE id = 1")  # CHECK fails
except sqlite3.IntegrityError as e:
    print("Transfer failed:", e)

print(conn.execute("SELECT owner, balance FROM accounts").fetchall())
# Transfer failed: CHECK constraint failed: balance >= 0
# [('Ada', 5000), ('Tunde', 1000)]
```

Tunde's credit **did** run, but the failed debit rolled the whole transaction back, so his balance is unchanged. Without `with conn:`, Tunde would keep ₦9,000 that came from nowhere (until the next commit made it permanent).

You can also raise your own exception inside the block to cancel it, for example when a check in Python fails:

```python
with conn:
    cur = conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 42")
    if cur.rowcount == 0:
        raise ValueError("no account 42")   # rolls back everything in this block
```

> **Note:** `with conn:` commits or rolls back, but it does **not** close the connection. Call `conn.close()` when you're done with it.

## 4. Schema design: one fact in one place

**Normalization** is the formal name for designing tables so that each fact is stored once. You don't need the textbook "normal forms"; three plain rules get you nearly all the way:

1. **One fact, one place.** If a customer's phone number appears in every order row, it will eventually be updated in some rows and not others.
2. **One value per column.** A `tags` column holding `"python,sql,web"` can't be joined, counted or constrained. Make a separate table with one row per tag.
3. **Link with ids.** Repeated groups of columns (a customer's name, email and phone repeated in each order) become their own table, linked by a foreign key.

Here's a table with problems:

```
orders
+----+---------------+-------------------+------------------+-----------------+
| id | customer_name | customer_email    | products         | total           |
+----+---------------+-------------------+------------------+-----------------+
|  1 | Ada Obi       | ada@example.com   | pen,notebook     | 2500            |
|  2 | Ada Obi       | ada@exmple.com    | stapler          | 1800            |
+----+---------------+-------------------+------------------+-----------------+
```

Ada's email is stored twice and already disagrees (a typo in row 2). `products` holds a list. And `total` can drift from the real sum of the items. A normalized design:

```
customers (id, name, email UNIQUE)
products  (id, name, price)
orders    (id, customer_id -> customers, created_on)
order_items (order_id -> orders, product_id -> products, quantity)
```

The total isn't stored at all; you compute it with a join and `SUM` when you need it. Sometimes teams **do** store a computed value for speed (that's called *denormalizing*), but it should be a deliberate choice, not an accident.

## 5. Indexes: the book's index, for tables

Without help, finding `WHERE customer_id = 42` means checking every row in the table, top to bottom. This is called a **full table scan**. For 100 rows that's instant; for 50 million rows it's slow.

An **index** is a separate, sorted structure that maps column values to the rows that have them, exactly like the index at the back of a book. Looking up a value becomes a quick search (roughly O(log n), from *Data structures, algorithms and Big-O*), not a scan of everything.

```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

Primary keys and `UNIQUE` columns get an index automatically. Other columns you filter or join on often (foreign keys especially) usually deserve one.

## 6. Asking the database how it will run a query

How do you know whether a query uses an index? Ask. `EXPLAIN QUERY PLAN` in front of a query shows SQLite's plan without running it:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total INTEGER)")

def plan(sql):
    return [row[3] for row in conn.execute("EXPLAIN QUERY PLAN " + sql)]

print(plan("SELECT * FROM orders WHERE customer_id = 42"))
# ['SCAN orders']

conn.execute("CREATE INDEX idx_orders_customer ON orders (customer_id)")
print(plan("SELECT * FROM orders WHERE customer_id = 42"))
# ['SEARCH orders USING INDEX idx_orders_customer (customer_id=?)']

print(plan("SELECT * FROM orders WHERE id = 7"))
# ['SEARCH orders USING INTEGER PRIMARY KEY (rowid=?)']
```

Each plan row is a tuple; the human-readable part is the fourth item (`row[3]`). Read it like this:

- **`SCAN orders`**: reads every row. Fine for small tables, a warning sign for big ones.
- **`SEARCH orders USING INDEX ...`**: jumps straight to matching rows with an index.
- **`USING COVERING INDEX`**: even better, the index alone holds every column the query needs.

PostgreSQL has the same idea with `EXPLAIN` and `EXPLAIN ANALYZE`; the wording differs, but "scan vs index" is the same question.

> **Try it:** in the practice editor, create the `orders` table above, then compare the plans for `WHERE total > 1000` before and after `CREATE INDEX idx_orders_total ON orders (total)`.

## 7. Indexes aren't free

If indexes make reads fast, why not index every column? Because every index must be updated on every `INSERT`, `UPDATE` and `DELETE`, and each one takes disk space. A table with ten indexes makes every write do eleven pieces of work. The usual approach:

- Index primary keys (automatic), foreign keys, and columns you filter, join or sort on in frequent queries.
- Don't index columns you rarely search, or with only a couple of distinct values (like a yes/no flag) in small tables.
- When a query is slow, look at its plan first, then add an index, then check the plan again. Measure; don't guess.

## Common mistakes

**`UPDATE` or `DELETE` without `WHERE`.** Covered above, and worth repeating because it's the classic production incident. Run the `WHERE` as a `SELECT` first.

**Forgetting to commit.** Changes made outside `with conn:` and never committed vanish when the connection closes. If your data "doesn't save", look for the missing commit.

**Catching the exception inside the transaction.** If you wrap one statement in `try/except` *inside* `with conn:` and swallow the error, the block ends normally and commits the half-done work. Let the exception leave the `with` block (or re-raise it) so the rollback happens.

**`database is locked`.** In SQLite, another connection holds an open transaction on a file database. Usually it's your own code: a connection that wrote something and never committed or closed. Keep transactions short.

**Adding an index and assuming it's used.** A query like `WHERE LOWER(email) = ?` can't use a plain index on `email`, because it searches a computed value. Check with `EXPLAIN QUERY PLAN`.

## Recap

- `INSERT` adds, `UPDATE ... SET ... WHERE` changes, `DELETE FROM ... WHERE` removes. No `WHERE` means every row.
- A **transaction** makes several statements all-or-nothing: `COMMIT` keeps them, `ROLLBACK` discards them.
- In Python, `with conn:` commits on success and rolls back on an exception.
- **Normalize**: one fact in one place, one value per column, link with ids.
- An **index** makes lookups fast; `EXPLAIN QUERY PLAN` shows `SCAN` (every row) vs `SEARCH ... USING INDEX`.
- Indexes slow writes and take space: add them where queries need them, and check the plan.
