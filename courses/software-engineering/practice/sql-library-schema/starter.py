import sqlite3


def create_library_schema(conn: sqlite3.Connection) -> None:
    """Turn on foreign keys for this connection and create authors, books, members and loans."""
    # TODO 1: switch on foreign-key enforcement for this connection
    # TODO 2: create the four tables, with REFERENCES for each link
    pass


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    create_library_schema(conn)
    try:
        conn.execute("INSERT INTO authors (id, name) VALUES (1, 'Chinua Achebe')")
        conn.execute("INSERT INTO books (title, author_id) VALUES ('Arrow of God', 1)")
        conn.execute("DELETE FROM authors WHERE id = 1")
        print("Oops: deleted an author who still has books")
    except sqlite3.Error as e:
        print(type(e).__name__, e)
