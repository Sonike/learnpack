import sqlite3

NEVER_BORROWED = """
    SELECT b.title
    FROM books AS b
    LEFT JOIN loans AS l ON l.book_id = b.id
    WHERE l.id IS NULL
    ORDER BY b.title
"""

LOANS_PER_AUTHOR = """
    SELECT a.name, COUNT(l.id) AS loan_count
    FROM authors AS a
    LEFT JOIN books AS b ON b.author_id = a.id
    LEFT JOIN loans AS l ON l.book_id = b.id
    GROUP BY a.id
    ORDER BY loan_count DESC, a.name
"""

# Uses one ? placeholder for today's date.
OVERDUE_MEMBERS = """
    SELECT DISTINCT m.name
    FROM loans AS l
    JOIN members AS m ON l.member_id = m.id
    WHERE l.returned_on IS NULL AND l.due_on < ?
    ORDER BY m.name
"""

SCHEMA = """
CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE books   (id INTEGER PRIMARY KEY, title TEXT NOT NULL,
                      author_id INTEGER NOT NULL REFERENCES authors(id));
CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE loans   (id INTEGER PRIMARY KEY,
                      book_id INTEGER NOT NULL REFERENCES books(id),
                      member_id INTEGER NOT NULL REFERENCES members(id),
                      loaned_on TEXT NOT NULL, due_on TEXT NOT NULL, returned_on TEXT);

INSERT INTO authors VALUES (1, 'Chinua Achebe'), (2, 'Chimamanda Ngozi Adichie'),
    (3, 'Wole Soyinka'), (4, 'Buchi Emecheta'), (5, 'Ben Okri');
INSERT INTO books VALUES (1, 'Things Fall Apart', 1), (2, 'Arrow of God', 1),
    (3, 'Purple Hibiscus', 2), (4, 'Americanah', 2), (5, 'Half of a Yellow Sun', 2),
    (6, 'Death and the King''s Horseman', 3), (7, 'The Joys of Motherhood', 4);
INSERT INTO members VALUES (1, 'Ada'), (2, 'Tunde'), (3, 'Zainab'), (4, 'Emeka');
INSERT INTO loans VALUES
    (1, 1, 1, '2026-01-10', '2026-01-24', '2026-01-20'),
    (2, 3, 2, '2026-02-01', '2026-02-15', NULL),
    (3, 1, 2, '2026-02-03', '2026-02-17', NULL),
    (4, 6, 3, '2026-02-20', '2026-03-06', NULL),
    (5, 4, 4, '2026-01-05', '2026-01-19', '2026-02-10'),
    (6, 5, 1, '2026-02-10', '2026-02-28', NULL),
    (7, 6, 4, '2026-01-02', '2026-01-16', '2026-01-15'),
    (8, 1, 3, '2026-02-15', '2026-03-01', NULL);
"""


def make_db() -> sqlite3.Connection:
    """A fresh in-memory library database with sample data."""
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    return conn


if __name__ == "__main__":
    conn = make_db()
    print(conn.execute(NEVER_BORROWED).fetchall())
    print(conn.execute(LOANS_PER_AUTHOR).fetchall())
    print(conn.execute(OVERDUE_MEMBERS, ("2026-03-01",)).fetchall())
    print(conn.execute(OVERDUE_MEMBERS, ("2026-03-10",)).fetchall())
