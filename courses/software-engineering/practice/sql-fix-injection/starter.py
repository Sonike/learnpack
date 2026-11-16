import sqlite3


def find_user(conn: sqlite3.Connection, name: str) -> dict | None:
    """The user named exactly `name`, as a dict, or None."""
    # TODO: this f-string is injectable. Use a ? parameter instead.
    row = conn.execute(f"SELECT id, name, email FROM users WHERE name = '{name}'").fetchone()
    if row is None:
        return None
    return {"id": row[0], "name": row[1], "email": row[2]}


def search_users(conn: sqlite3.Connection, text: str) -> list[str]:
    """Names containing `text` (any case), sorted A to Z."""
    # TODO: this f-string is injectable too. Put the % signs in the value, not the SQL.
    rows = conn.execute(f"SELECT name FROM users WHERE name LIKE '%{text}%' ORDER BY name")
    return [row[0] for row in rows]


def make_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL)")
    conn.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        [
            ("Ada", "ada@example.com"),
            ("Tunde", "tunde@example.com"),
            ("O'Brien", "obrien@example.com"),
            ("Adaeze", "adaeze@example.com"),
            ("Chinedu Adamu", "chinedu@example.com"),
        ],
    )
    return conn


if __name__ == "__main__":
    conn = make_db()
    print(find_user(conn, "Ada"))
    print(find_user(conn, "' OR '1'='1"))   # the current code returns a user it shouldn't!
    print(search_users(conn, "ad"))
    try:
        print(find_user(conn, "O'Brien"))
    except sqlite3.Error as e:
        print("O'Brien crashed it:", e)
