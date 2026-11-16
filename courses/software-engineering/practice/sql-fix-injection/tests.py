import sqlite3

from solution import find_user, search_users


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


def test_finds_a_user_by_exact_name():
    got = find_user(make_db(), "Tunde")
    want = {"id": 2, "name": "Tunde", "email": "tunde@example.com"}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_handles_a_name_with_an_apostrophe():
    got = find_user(make_db(), "O'Brien")
    want = {"id": 3, "name": "O'Brien", "email": "obrien@example.com"}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_injection_in_find_user_returns_none():
    got = find_user(make_db(), "' OR '1'='1")
    assert got is None, f"expected None, got {got!r}"


def test_search_finds_names_containing_the_text():
    got = search_users(make_db(), "ad")
    want = ["Ada", "Adaeze", "Chinedu Adamu"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_search_handles_quotes_and_injection():
    conn = make_db()
    got = search_users(conn, "'B")
    want = ["O'Brien"]
    assert got == want, f"expected {want!r}, got {got!r}"
    got = search_users(conn, "' OR '1'='1")
    assert got == [], f"expected {[]!r}, got {got!r}"
