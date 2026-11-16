# Five questions for a films table

You're the data person for a film club. Answer five questions by writing **SQL strings**. Each answer is a constant in `solution.py`; the tests run it against the `films` table and compare the rows exactly, including column order and row order.

The table (the starter's `make_db()` builds it with 17 films, so you can try your queries):

```
films(id INTEGER PRIMARY KEY, title TEXT, year INTEGER, genre TEXT, rating REAL, runtime INTEGER)
```

`year` and `rating` can be `NULL` (one film has an unknown year and rating).

| Constant | Question | Columns, in order | Row order |
|---|---|---|---|
| `TOP_RATED_AFTER_2010` | The 5 highest-rated films released **after** 2010 (2010 itself doesn't count) | `title`, `rating` | rating high→low, ties by title A→Z |
| `COUNT_PER_GENRE` | How many films each genre has | `genre`, `film_count` | count high→low, ties by genre A→Z |
| `AVG_RUNTIME_BY_DECADE` | Average runtime per decade (2004 → 2000, 2016 → 2010), rounded to 1 decimal place; skip films with no year | `decade`, `avg_runtime` | decade low→high |
| `TITLES_WITH_NIGHT` | Titles containing "night" anywhere, in any case (yes, "Knight" counts) | `title` | A→Z |
| `BIG_GENRES` | Genres with **more than 3** films | `genre`, `film_count` | genre A→Z |

Hints: `ORDER BY ... DESC, ...`, `LIMIT`, `GROUP BY`, `HAVING`, `LIKE '%...%'`, `ROUND(x, 1)`, and integer division `(year / 10) * 10`.

## Example

```python
conn = make_db()
conn.execute(TOP_RATED_AFTER_2010).fetchall()
# [('Parasite', 8.5), ('Mad Max: Fury Road', 8.1), ('Dune', 8.0), ('Arrival', 7.9), ('Knives Out', 7.9)]
```
