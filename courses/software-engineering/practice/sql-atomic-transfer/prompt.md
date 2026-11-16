# An all-or-nothing money transfer

Write `transfer(conn, from_id, to_id, amount)` that moves money between two bank accounts **atomically**: either the whole transfer happens, or nothing changes at all.

```python
def transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: int) -> None: ...
```

- `conn`: an open connection with this table (the starter's `make_db()` creates it):
  ```sql
  CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT NOT NULL,
                         balance INTEGER NOT NULL CHECK (balance >= 0))
  ```
- `from_id`, `to_id`: the account ids to take money from and give it to.
- `amount`: a whole number of naira.

Rules:

1. If `amount` is 0 or negative, raise `ValueError` and change nothing.
2. **Add to the receiver first, then take from the sender** (this order is deliberate: it makes atomicity matter).
3. If either account doesn't exist (an `UPDATE` changed 0 rows), raise `ValueError`, and nothing may change.
4. If the sender doesn't have enough money, the `CHECK` constraint raises `sqlite3.IntegrityError`. Let it propagate, and nothing may change.
5. A successful transfer is committed.

Hint: do both `UPDATE`s inside one `with conn:` block. `cursor.rowcount` tells you how many rows an `UPDATE` changed. Raising inside the block rolls everything back.

## Example

```python
conn = make_db()   # Ada (id 1) has 5000, Tunde (id 2) has 1000
transfer(conn, 1, 2, 2000)
balances(conn)     # {1: 3000, 2: 3000}
transfer(conn, 2, 1, 999_999)
# sqlite3.IntegrityError: CHECK constraint failed: balance >= 0
balances(conn)     # {1: 3000, 2: 3000}   (unchanged: Ada wasn't credited)
```
