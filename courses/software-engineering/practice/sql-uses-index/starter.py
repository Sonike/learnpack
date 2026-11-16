import sqlite3


def uses_index(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> bool:
    """True if SQLite's plan for `sql` uses an index (not just a table scan or the primary key)."""
    # TODO: run "EXPLAIN QUERY PLAN " + sql with params, and look at row[3] of each row
    return False


def add_index(conn: sqlite3.Connection) -> None:
    """Create the index that SLOW_QUERY needs, named idx_orders_customer."""
    # TODO: CREATE INDEX ...
    pass


SLOW_QUERY = "SELECT id, total FROM orders WHERE customer_id = ?"


def make_db() -> sqlite3.Connection:
    """An orders table with 1000 rows and no extra indexes."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, "
        "total INTEGER NOT NULL, status TEXT NOT NULL)"
    )
    conn.executemany(
        "INSERT INTO orders (customer_id, total, status) VALUES (?, ?, ?)",
        [(i % 50, (i * 37) % 9000, "paid" if i % 3 else "pending") for i in range(1000)],
    )
    conn.commit()
    return conn


if __name__ == "__main__":
    conn = make_db()
    for row in conn.execute("EXPLAIN QUERY PLAN " + SLOW_QUERY, (7,)):
        print("plan line:", row[3])
    print("uses an index before:", uses_index(conn, SLOW_QUERY, (7,)))
    add_index(conn)
    print("uses an index after:", uses_index(conn, SLOW_QUERY, (7,)))
