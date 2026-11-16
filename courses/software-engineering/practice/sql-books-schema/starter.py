import sqlite3


def create_schema(conn: sqlite3.Connection) -> None:
    """Create the books table with a primary key, NOT NULL, UNIQUE and CHECK rules."""
    # TODO: write a CREATE TABLE books (...) statement and run it with conn.execute
    pass


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    try:
        conn.execute(
            "INSERT INTO books (title, author, year, pages, isbn) "
            "VALUES ('Arrow of God', 'Chinua Achebe', 1964, 230, '978-0385014809')"
        )
        print(conn.execute("SELECT * FROM books").fetchall())
        conn.execute("INSERT INTO books (title, author, pages) VALUES ('Untitled', 'Anon', 0)")
        print("Oops: a book with 0 pages was accepted")
    except sqlite3.Error as e:
        print(type(e).__name__, e)
