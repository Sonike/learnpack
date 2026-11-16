import sqlite3

from solution import create_schema

INSERT = "INSERT INTO books (title, author, year, pages, isbn) VALUES (?, ?, ?, ?, ?)"


def fresh():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    return conn


def refused(conn, row):
    try:
        conn.execute(INSERT, row)
    except sqlite3.IntegrityError:
        return True
    return False


def test_accepts_a_valid_book_and_fills_in_the_id():
    conn = fresh()
    conn.execute(INSERT, ("Arrow of God", "Chinua Achebe", 1964, 230, "978-0385014809"))
    got = conn.execute("SELECT id, title, author, year, pages, isbn FROM books").fetchall()
    want = [(1, "Arrow of God", "Chinua Achebe", 1964, 230, "978-0385014809")]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_year_and_isbn_are_optional():
    conn = fresh()
    conn.execute(INSERT, ("Oral Tales", "Unknown", None, 90, None))
    conn.execute(INSERT, ("More Tales", "Unknown", None, 80, None))
    got = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    assert got == 2, f"expected {2!r}, got {got!r}"


def test_rejects_missing_or_empty_title_and_missing_author():
    conn = fresh()
    assert refused(conn, (None, "Achebe", 1958, 200, None)), "a NULL title was accepted"
    assert refused(conn, ("", "Achebe", 1958, 200, None)), "an empty title was accepted"
    assert refused(conn, ("Things Fall Apart", None, 1958, 200, None)), "a NULL author was accepted"


def test_rejects_zero_negative_or_missing_pages():
    conn = fresh()
    assert refused(conn, ("A", "B", 2000, 0, None)), "0 pages was accepted"
    assert refused(conn, ("A", "B", 2000, -10, None)), "negative pages were accepted"
    assert refused(conn, ("A", "B", 2000, None, None)), "missing pages were accepted"


def test_rejects_years_outside_1450_to_2100():
    conn = fresh()
    assert refused(conn, ("A", "B", 1449, 10, None)), "year 1449 was accepted"
    assert refused(conn, ("A", "B", 2101, 10, None)), "year 2101 was accepted"
    conn.execute(INSERT, ("Edge", "B", 1450, 10, None))
    conn.execute(INSERT, ("Edge 2", "B", 2100, 10, None))


def test_rejects_duplicate_isbn_and_duplicate_id():
    conn = fresh()
    conn.execute(INSERT, ("A", "B", 2000, 10, "123"))
    assert refused(conn, ("C", "D", 2001, 10, "123")), "a duplicate ISBN was accepted"
    try:
        conn.execute("INSERT INTO books (id, title, author, pages) VALUES (1, 'X', 'Y', 5)")
        ok = False
    except sqlite3.IntegrityError:
        ok = True
    assert ok, "a duplicate id was accepted"
