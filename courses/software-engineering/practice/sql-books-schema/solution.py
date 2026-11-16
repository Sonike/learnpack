import sqlite3


def create_schema(conn: sqlite3.Connection) -> None:
    """Create the books table with a primary key, NOT NULL, UNIQUE and CHECK rules."""
    conn.execute(
        """
        CREATE TABLE books (
            id     INTEGER PRIMARY KEY,
            title  TEXT    NOT NULL CHECK (title != ''),
            author TEXT    NOT NULL,
            year   INTEGER CHECK (year BETWEEN 1450 AND 2100),
            pages  INTEGER NOT NULL CHECK (pages > 0),
            isbn   TEXT    UNIQUE
        )
        """
    )


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    conn.execute(
        "INSERT INTO books (title, author, year, pages, isbn) "
        "VALUES ('Arrow of God', 'Chinua Achebe', 1964, 230, '978-0385014809')"
    )
    print(conn.execute("SELECT * FROM books").fetchall())
