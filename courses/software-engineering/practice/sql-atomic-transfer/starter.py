import sqlite3


def transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: int) -> None:
    """Move `amount` from account `from_id` to account `to_id`, all or nothing."""
    # TODO 1: reject amounts that are 0 or negative with ValueError
    # TODO 2: inside `with conn:`, add to the receiver, then take from the sender
    # TODO 3: if either UPDATE changed 0 rows, raise ValueError (this rolls back)
    pass


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
    print("before:", balances(conn))
    transfer(conn, 1, 2, 2000)
    print("after a good transfer:", balances(conn))
    try:
        transfer(conn, 2, 1, 999_999)
    except sqlite3.IntegrityError as e:
        print("refused:", e)
    print("after a failed transfer:", balances(conn))
