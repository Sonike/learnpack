import sqlite3


def create_library_schema(conn: sqlite3.Connection) -> None:
    """Turn on foreign keys for this connection and create authors, books, members and loans."""
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(
        """
        CREATE TABLE authors (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE books (
            id        INTEGER PRIMARY KEY,
            title     TEXT NOT NULL,
            author_id INTEGER NOT NULL REFERENCES authors(id)
        );
        CREATE TABLE members (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE loans (
            id          INTEGER PRIMARY KEY,
            book_id     INTEGER NOT NULL REFERENCES books(id),
            member_id   INTEGER NOT NULL REFERENCES members(id),
            loaned_on   TEXT NOT NULL,
            due_on      TEXT NOT NULL,
            returned_on TEXT
        );
        """
    )


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    create_library_schema(conn)
    conn.execute("INSERT INTO authors (id, name) VALUES (1, 'Chinua Achebe')")
    conn.execute("INSERT INTO books (title, author_id) VALUES ('Arrow of God', 1)")
    try:
        conn.execute("DELETE FROM authors WHERE id = 1")
    except sqlite3.IntegrityError as e:
        print("Refused:", e)
