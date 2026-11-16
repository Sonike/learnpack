import sqlite3


def transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: int) -> None:
    """Move `amount` from account `from_id` to account `to_id`, all or nothing."""
    if amount <= 0:
        raise ValueError("amount must be positive")
    with conn:  # commits on success, rolls back if anything below raises
        credited = conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id)
        )
        if credited.rowcount == 0:
            raise ValueError(f"no account {to_id}")
        debited = conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id)
        )
        if debited.rowcount == 0:
            raise ValueError(f"no account {from_id}")


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


if __name__ == "__main__":
    conn = make_db()
    transfer(conn, 1, 2, 2000)
    print(balances(conn))
