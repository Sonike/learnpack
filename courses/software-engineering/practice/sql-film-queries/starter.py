import sqlite3

# TODO: replace each "" with your SQL query (triple-quoted strings work well).

TOP_RATED_AFTER_2010 = ""

COUNT_PER_GENRE = ""

AVG_RUNTIME_BY_DECADE = ""

TITLES_WITH_NIGHT = ""

BIG_GENRES = ""


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


if __name__ == "__main__":
    conn = make_db()
    for name in ["TOP_RATED_AFTER_2010", "COUNT_PER_GENRE", "AVG_RUNTIME_BY_DECADE", "TITLES_WITH_NIGHT", "BIG_GENRES"]:
        sql = globals()[name]
        print(name)
        if not sql.strip():
            print("  (not written yet)")
            continue
        for row in conn.execute(sql):
            print("  ", row)
