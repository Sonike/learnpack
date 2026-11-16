import sqlite3

TOP_RATED_AFTER_2010 = """
    SELECT title, rating
    FROM films
    WHERE year > 2010
    ORDER BY rating DESC, title
    LIMIT 5
"""

COUNT_PER_GENRE = """
    SELECT genre, COUNT(*) AS film_count
    FROM films
    GROUP BY genre
    ORDER BY film_count DESC, genre
"""

AVG_RUNTIME_BY_DECADE = """
    SELECT (year / 10) * 10 AS decade, ROUND(AVG(runtime), 1) AS avg_runtime
    FROM films
    WHERE year IS NOT NULL
    GROUP BY decade
    ORDER BY decade
"""

TITLES_WITH_NIGHT = """
    SELECT title
    FROM films
    WHERE title LIKE '%night%'
    ORDER BY title
"""

BIG_GENRES = """
    SELECT genre, COUNT(*) AS film_count
    FROM films
    GROUP BY genre
    HAVING COUNT(*) > 3
    ORDER BY genre
"""


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
    for sql in [TOP_RATED_AFTER_2010, COUNT_PER_GENRE, AVG_RUNTIME_BY_DECADE, TITLES_WITH_NIGHT, BIG_GENRES]:
        print(conn.execute(sql).fetchall())
