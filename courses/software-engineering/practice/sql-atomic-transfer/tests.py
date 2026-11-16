import sqlite3

from solution import transfer


def make_db() -> sqlite3.Connection:
    """Two accounts: Ada (id 1) with 5000 and Tunde (id 2) with 1000."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, "
        "balance INTEGER NOT NULL CHECK (balance >= 0))"
    )
    conn.execute("INSERT INTO accounts (id, owner, balance) VALUES (1, 'Ada', 5000), (2, 'Tunde', 1000)")
    conn.commit()
    return conn


def balances(conn: sqlite3.Connection) -> dict[int, int]:
    return dict(conn.execute("SELECT id, balance FROM accounts ORDER BY id").fetchall())


def raises(exc_type, fn, *args):
    try:
        fn(*args)
    except exc_type:
        return True
    return False


def test_moves_money_between_accounts():
    conn = make_db()
    transfer(conn, 1, 2, 2000)
    got = balances(conn)
    want = {1: 3000, 2: 3000}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_a_successful_transfer_is_committed():
    conn = make_db()
    transfer(conn, 1, 2, 500)
    assert not conn.in_transaction, "the transfer was left uncommitted (missing commit / with conn:)"
    conn.rollback()  # nothing should be left to undo
    got = balances(conn)
    want = {1: 4500, 2: 1500}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_insufficient_funds_changes_nothing():
    conn = make_db()
    assert raises(sqlite3.IntegrityError, transfer, conn, 2, 1, 999_999), "expected sqlite3.IntegrityError"
    got = balances(conn)
    want = {1: 5000, 2: 1000}
    assert got == want, f"expected {want!r} (Ada must not keep the credit), got {got!r}"


def test_missing_sender_changes_nothing():
    conn = make_db()
    assert raises(ValueError, transfer, conn, 42, 2, 100), "expected ValueError for a missing sender"
    got = balances(conn)
    want = {1: 5000, 2: 1000}
    assert got == want, f"expected {want!r} (Tunde must not keep the credit), got {got!r}"


def test_missing_receiver_changes_nothing():
    conn = make_db()
    assert raises(ValueError, transfer, conn, 1, 42, 100), "expected ValueError for a missing receiver"
    got = balances(conn)
    want = {1: 5000, 2: 1000}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_rejects_zero_and_negative_amounts():
    conn = make_db()
    assert raises(ValueError, transfer, conn, 1, 2, 0), "expected ValueError for amount 0"
    assert raises(ValueError, transfer, conn, 1, 2, -500), "expected ValueError for a negative amount"
    got = balances(conn)
    want = {1: 5000, 2: 1000}
    assert got == want, f"expected {want!r}, got {got!r}"
