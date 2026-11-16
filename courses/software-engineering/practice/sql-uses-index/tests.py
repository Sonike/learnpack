import sqlite3

from solution import add_index, uses_index

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


def test_a_full_scan_does_not_use_an_index():
    got = uses_index(make_db(), SLOW_QUERY, (7,))
    assert got is False, f"expected {False!r}, got {got!r}"


def test_a_primary_key_lookup_does_not_count():
    got = uses_index(make_db(), "SELECT total FROM orders WHERE id = ?", (5,))
    assert got is False, f"expected {False!r}, got {got!r}"


def test_detects_an_index_and_a_covering_index():
    conn = make_db()
    conn.execute("CREATE INDEX idx_orders_status ON orders (status)")
    got = uses_index(conn, "SELECT * FROM orders WHERE status = ?", ("pending",))
    assert got is True, f"expected {True!r} for USING INDEX, got {got!r}"
    got = uses_index(conn, "SELECT status FROM orders WHERE status = 'paid'")
    assert got is True, f"expected {True!r} for USING COVERING INDEX, got {got!r}"


def test_an_index_on_another_column_does_not_help():
    conn = make_db()
    conn.execute("CREATE INDEX idx_orders_status ON orders (status)")
    got = uses_index(conn, SLOW_QUERY, (7,))
    assert got is False, f"expected {False!r}, got {got!r}"


def test_add_index_makes_the_slow_query_use_it():
    conn = make_db()
    add_index(conn)
    got = uses_index(conn, SLOW_QUERY, (7,))
    assert got is True, f"expected {True!r}, got {got!r}"
    names = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'index'")]
    assert "idx_orders_customer" in names, f"expected an index named 'idx_orders_customer', got {names!r}"


def test_add_index_does_not_change_the_results():
    conn = make_db()
    before = conn.execute(SLOW_QUERY + " ORDER BY id", (7,)).fetchall()
    add_index(conn)
    after = conn.execute(SLOW_QUERY + " ORDER BY id", (7,)).fetchall()
    assert after == before, f"expected the same {len(before)} rows, got {len(after)}"
