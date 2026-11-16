import sqlite3

import solution

FILMS = [
    ("The Wedding Party", 2016, "Comedy", 7.1, 110),
    ("Lionheart", 2018, "Comedy", 5.9, 95),
    ("Night Watch", 2004, "Fantasy", 6.4, 114),
    ("Inception", 2010, "Sci-Fi", 8.8, 148),
    ("Arrival", 2016, "Sci-Fi", 7.9, 116),
    ("Midnight in Paris", 2011, "Comedy", 7.6, 94),
    ("The Dark Knight", 2008, "Action", 9.0, 152),
    ("Mad Max: Fury Road", 2015, "Action", 8.1, 120),
    ("King of Boys", 2018, "Drama", 7.5, 169),
    ("Nightcrawler", 2014, "Drama", 7.8, 117),
    ("Moonlight", 2016, "Drama", 7.4, 111),
    ("Isoken", 2017, "Comedy", 6.8, 108),
    ("Dune", 2021, "Sci-Fi", 8.0, 155),
    ("Black Panther", 2018, "Action", 7.3, 134),
    ("Knives Out", 2019, "Comedy", 7.9, 130),
    ("Unknown Title", None, "Drama", None, 101),
    ("Parasite", 2019, "Drama", 8.5, 132),
]


def make_db() -> sqlite3.Connection:
    """A fresh in-memory database with the films table filled in."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT NOT NULL, year INTEGER, "
        "genre TEXT NOT NULL, rating REAL, runtime INTEGER NOT NULL)"
    )
    conn.executemany(
        "INSERT INTO films (title, year, genre, rating, runtime) VALUES (?, ?, ?, ?, ?)", FILMS
    )
    return conn


def run(name):
    sql = getattr(solution, name)
    assert sql.strip(), f"{name} is still empty"
    return make_db().execute(sql).fetchall()


def test_top_rated_after_2010():
    got = run("TOP_RATED_AFTER_2010")
    want = [("Parasite", 8.5), ("Mad Max: Fury Road", 8.1), ("Dune", 8.0), ("Arrival", 7.9), ("Knives Out", 7.9)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_count_per_genre():
    got = run("COUNT_PER_GENRE")
    want = [("Comedy", 5), ("Drama", 5), ("Action", 3), ("Sci-Fi", 3), ("Fantasy", 1)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_average_runtime_by_decade_skips_unknown_years():
    got = run("AVG_RUNTIME_BY_DECADE")
    want = [(2000, 133.0), (2010, 121.8), (2020, 155.0)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_titles_with_night_in_any_case():
    got = run("TITLES_WITH_NIGHT")
    want = [("Midnight in Paris",), ("Night Watch",), ("Nightcrawler",), ("The Dark Knight",)]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_genres_with_more_than_three_films():
    got = run("BIG_GENRES")
    want = [("Comedy", 5), ("Drama", 5)]
    assert got == want, f"expected {want!r}, got {got!r}"
