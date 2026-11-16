# Does this query use an index?

Write two functions: one that reads SQLite's query plan to tell whether a query uses an index, and one that adds the index a slow query needs.

```python
def uses_index(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> bool: ...
def add_index(conn: sqlite3.Connection) -> None: ...
```

### `uses_index`

- `conn`: an open connection. `sql`: a `SELECT` query. `params`: values for any `?` placeholders in `sql`.
- Run `"EXPLAIN QUERY PLAN " + sql` with `params`. Each result row is a tuple whose **fourth item** (`row[3]`) is a line of the plan, such as:
  - `'SCAN orders'`: reads every row
  - `'SEARCH orders USING INDEX idx_orders_customer (customer_id=?)'`
  - `'SEARCH orders USING COVERING INDEX idx_orders_customer (customer_id=?)'`
  - `'SEARCH orders USING INTEGER PRIMARY KEY (rowid=?)'`
- Return `True` if **any** plan line contains `"USING INDEX"` or `"USING COVERING INDEX"`, otherwise `False`. (A primary-key lookup doesn't count: we're checking for indexes you created.)

### `add_index`

The app runs `SLOW_QUERY` (in the starter) on every page view:

```sql
SELECT id, total FROM orders WHERE customer_id = ?
```

Write `add_index(conn)` so that, after it runs, `uses_index(conn, SLOW_QUERY, (7,))` is `True`. Name your index `idx_orders_customer`.

## Example

```python
conn = make_db()
uses_index(conn, SLOW_QUERY, (7,))   # False  (plan: SCAN orders)
add_index(conn)
uses_index(conn, SLOW_QUERY, (7,))   # True   (plan: SEARCH orders USING INDEX idx_orders_customer ...)
```
