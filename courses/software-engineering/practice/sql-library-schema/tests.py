import sqlite3

from solution import create_library_schema


def fresh():
    conn = sqlite3.connect(":memory:")
    create_library_schema(conn)
    conn.execute("INSERT INTO authors (id, name) VALUES (1, 'Chinua Achebe'), (2, 'Ben Okri')")
    conn.execute("INSERT INTO books (id, title, author_id) VALUES (10, 'Arrow of God', 1)")
    conn.execute("INSERT INTO members (id, name) VALUES (100, 'Ada')")
    return conn


def refused(conn, sql):
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError:
        return True
    return False


def test_valid_rows_are_accepted():
    conn = fresh()
    conn.execute(
        "INSERT INTO loans (book_id, member_id, loaned_on, due_on) "
        "VALUES (10, 100, '2026-02-01', '2026-02-15')"
    )
    got = conn.execute("SELECT book_id, member_id, returned_on FROM loans").fetchall()
    want = [(10, 100, None)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_rejects_a_book_by_a_missing_author():
    conn = fresh()
    assert refused(conn, "INSERT INTO books (title, author_id) VALUES ('Ghost', 99)"), \
        "a book pointing at author 99 (who doesn't exist) was accepted: is PRAGMA foreign_keys on?"
    assert refused(conn, "INSERT INTO books (title, author_id) VALUES ('Ghost', NULL)"), \
        "a book with no author_id was accepted"


def test_deleting_an_author_with_books_fails():
    conn = fresh()
    assert refused(conn, "DELETE FROM authors WHERE id = 1"), \
        "deleted an author who still has books"


def test_deleting_an_author_without_books_works():
    conn = fresh()
    conn.execute("DELETE FROM authors WHERE id = 2")
    got = conn.execute("SELECT name FROM authors").fetchall()
    want = [("Chinua Achebe",)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_rejects_loans_for_missing_member_or_book():
    conn = fresh()
    assert refused(conn, "INSERT INTO loans (book_id, member_id, loaned_on, due_on) "
                         "VALUES (10, 999, '2026-02-01', '2026-02-15')"), "a loan for member 999 was accepted"
    assert refused(conn, "INSERT INTO loans (book_id, member_id, loaned_on, due_on) "
                         "VALUES (999, 100, '2026-02-01', '2026-02-15')"), "a loan for book 999 was accepted"
