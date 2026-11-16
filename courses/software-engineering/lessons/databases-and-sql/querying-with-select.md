# Querying with SELECT

## Why this matters

Storing data is only half the job; the other half is asking it questions. "Which customers haven't ordered this month?", "What's our average delivery time per city?", "Which songs were played more than 100 times?" Each is one `SELECT` statement. You'll write queries like these to build features, to debug ("how many users have a null email?"), and in interviews. A good query replaces dozens of lines of Python loops, and runs far faster.

All examples in this lesson use this small table:

```
films
+----+---------------------+------+---------+--------+---------+
| id | title               | year | genre   | rating | runtime |
+----+---------------------+------+---------+--------+---------+
|  1 | The Wedding Party   | 2016 | Comedy  |    7.1 |     110 |
|  2 | Lionheart           | 2018 | Comedy  |    5.9 |      95 |
|  3 | Night Watch         | 2004 | Fantasy |    6.4 |     114 |
|  4 | Inception           | 2010 | Sci-Fi  |    8.8 |     148 |
|  5 | Arrival             | 2016 | Sci-Fi  |    7.9 |     116 |
|  6 | Midnight in Paris   | 2011 | Comedy  |    7.6 |      94 |
|  7 | Unknown Title       | NULL | Drama   |   NULL |     101 |
+----+---------------------+------+---------+--------+---------+
```

> **Try it:** paste this into the practice editor to follow along. Change the queries and predict the output before you run.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, genre TEXT, rating REAL, runtime INTEGER)")
conn.executemany(
    "INSERT INTO films (title, year, genre, rating, runtime) VALUES (?, ?, ?, ?, ?)",
    [
        ("The Wedding Party", 2016, "Comedy", 7.1, 110),
        ("Lionheart", 2018, "Comedy", 5.9, 95),
        ("Night Watch", 2004, "Fantasy", 6.4, 114),
        ("Inception", 2010, "Sci-Fi", 8.8, 148),
        ("Arrival", 2016, "Sci-Fi", 7.9, 116),
        ("Midnight in Paris", 2011, "Comedy", 7.6, 94),
        ("Unknown Title", None, "Drama", None, 101),
    ],
)

def show(sql):
    for row in conn.execute(sql):
        print(row)

show("SELECT title FROM films WHERE year > 2015")
```

`executemany` runs the same `INSERT` once per tuple. The `?` marks are **placeholders** that get filled with each tuple's values; *SQL from Python, safely* explains why they matter so much.

## 1. SELECT and FROM

The simplest query names the columns you want and the table they come from:

```sql
SELECT title, year FROM films;
-- ('The Wedding Party', 2016)
-- ('Lionheart', 2018)
-- ... one row per film
```

`SELECT *` returns every column. It's handy for exploring, but in program code list the columns you need: it's clearer, and your code won't break when someone adds a column.

You can also compute values:

```sql
SELECT title, runtime / 60.0 AS hours FROM films WHERE id = 4;
-- ('Inception', 2.466666666666667)
```

`AS hours` gives the computed column a name, called an **alias**. Note `60.0`: in SQLite, `148 / 60` is integer division and gives `2`, just like `148 // 60` in Python.

## 2. Filtering rows with WHERE

`WHERE` keeps only the rows where a condition is true:

```sql
SELECT title FROM films WHERE genre = 'Comedy';
-- ('The Wedding Party',) ('Lionheart',) ('Midnight in Paris',)
```

SQL uses a single `=` for comparison (there's no assignment in a `WHERE`). Not-equal is `!=` or `<>`. Combine conditions with `AND`, `OR` and `NOT`, and use brackets to make the order clear:

```sql
SELECT title FROM films
WHERE genre = 'Comedy' AND (rating > 7 OR runtime < 100);
-- ('The Wedding Party',) ('Lionheart',) ('Midnight in Paris',)
```

Lionheart is in there because its runtime is 95, even though its rating is low.

Three shortcuts you'll use constantly:

```sql
SELECT title FROM films WHERE year BETWEEN 2010 AND 2016;   -- inclusive at both ends
-- Wedding Party, Inception, Arrival, Midnight in Paris

SELECT title FROM films WHERE genre IN ('Sci-Fi', 'Fantasy');
-- Night Watch, Inception, Arrival

SELECT title FROM films WHERE title LIKE '%night%';
-- ('Night Watch',) ('Midnight in Paris',)
```

`LIKE` matches text patterns: `%` means "any number of characters" and `_` means "exactly one character". So `'%night%'` means "contains night anywhere". In SQLite, `LIKE` ignores upper and lower case for English letters, which is why it found "Night Watch". (PostgreSQL's `LIKE` is case-sensitive; it has `ILIKE` for the case-insensitive version.)

## 3. NULL: the value that isn't there

Look at "Unknown Title": its year and rating are `NULL`, meaning unknown. Watch this:

```sql
SELECT title FROM films WHERE rating = NULL;
-- (no rows!)

SELECT title FROM films WHERE rating IS NULL;
-- ('Unknown Title',)
```

Why does `= NULL` find nothing? Because `NULL` means "unknown", and "is this unknown value equal to unknown?" has the answer *unknown*, not *true*. `WHERE` only keeps rows where the condition is **true**, so every row is dropped. Always use `IS NULL` and `IS NOT NULL`.

The same logic means `NULL` rows quietly fall out of other filters too: `WHERE rating < 7` doesn't include "Unknown Title", and neither does `WHERE rating >= 7`. When numbers seem to be missing from a report, check for `NULL`s first.

## 4. Sorting and limiting

Rows come back in no guaranteed order unless you ask. `ORDER BY` sorts; add `DESC` for largest-first. `LIMIT` keeps the first N rows:

```sql
SELECT title, rating FROM films
WHERE rating IS NOT NULL
ORDER BY rating DESC
LIMIT 3;
-- ('Inception', 8.8)
-- ('Arrival', 7.9)
-- ('Midnight in Paris', 7.6)
```

You can sort by several columns: `ORDER BY year DESC, title` sorts by year (newest first), and films from the same year alphabetically. This "tie-breaker" matters whenever you want a stable, predictable order, for example in tests.

The order you **write** the clauses is fixed:

```
SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT ...
```

## 5. Aggregates: one answer from many rows

An **aggregate function** squashes many rows into one value:

| Function | Returns |
|---|---|
| `COUNT(*)` | number of rows |
| `COUNT(col)` | number of rows where `col` is not `NULL` |
| `SUM(col)` | total |
| `AVG(col)` | average |
| `MIN(col)` / `MAX(col)` | smallest / largest |

```sql
SELECT COUNT(*), COUNT(rating), AVG(runtime), MAX(rating) FROM films;
-- (7, 6, 111.14285714285714, 8.8)
```

Notice `COUNT(rating)` is 6, not 7: aggregates skip `NULL`s. `AVG(rating)` is the average of the six known ratings, not seven. Use `ROUND(AVG(runtime), 1)` to get `111.1`.

## 6. GROUP BY: one answer per group

Often you want an aggregate *per* something: films per genre, sales per month. `GROUP BY` splits the rows into groups that share a value, then runs the aggregate once per group:

```sql
SELECT genre, COUNT(*) AS film_count, ROUND(AVG(rating), 2) AS avg_rating
FROM films
GROUP BY genre
ORDER BY film_count DESC, genre;
-- ('Comedy', 3, 6.87)
-- ('Sci-Fi', 2, 8.35)
-- ('Drama', 1, None)
-- ('Fantasy', 1, 6.4)
```

Picture it like this:

```
rows ──GROUP BY genre──►  Comedy:  Wedding Party, Lionheart, Midnight  ──► 3
                          Sci-Fi:  Inception, Arrival                  ──► 2
                          Drama:   Unknown Title                       ──► 1
                          Fantasy: Night Watch                         ──► 1
```

Rule of thumb: every column in the `SELECT` must either be in the `GROUP BY` or be inside an aggregate. Selecting `title` here makes no sense (which of the three comedy titles?). PostgreSQL rejects it; SQLite quietly picks one row's value, which is a classic source of wrong reports.

You can group by a computed value too. Integer division gives each film's decade:

```sql
SELECT (year / 10) * 10 AS decade, COUNT(*) FROM films
WHERE year IS NOT NULL
GROUP BY decade
ORDER BY decade;
-- (2000, 1)
-- (2010, 5)
```

## 7. HAVING: filtering groups

`WHERE` filters **rows before** grouping. `HAVING` filters **groups after** grouping, so it can use aggregates:

```sql
SELECT genre, COUNT(*) AS film_count
FROM films
GROUP BY genre
HAVING COUNT(*) >= 2;
-- ('Comedy', 3)
-- ('Sci-Fi', 2)
```

You can use both in one query. "Genres with at least two films released after 2010":

```sql
SELECT genre, COUNT(*)
FROM films
WHERE year > 2010            -- 1. drop old films
GROUP BY genre               -- 2. group what's left
HAVING COUNT(*) >= 2;        -- 3. drop small groups
-- ('Comedy', 3)
```

Sci-Fi drops out because Inception (2010) was removed by `WHERE` before counting.

## 8. Running queries from Python

Each query you write is just a string. You've already seen the pattern:

```python
TOP_THREE = """
    SELECT title, rating FROM films
    WHERE rating IS NOT NULL
    ORDER BY rating DESC
    LIMIT 3
"""
print(conn.execute(TOP_THREE).fetchall())
# [('Inception', 8.8), ('Arrival', 7.9), ('Midnight in Paris', 7.6)]
```

Triple-quoted strings let you lay the query out over several lines, which makes long queries far easier to read and review. The practice exercise works exactly like this: you write the SQL strings, and the tests run them.

## Common mistakes

**`WHERE` with an aggregate.**

```sql
SELECT genre FROM films WHERE COUNT(*) > 2 GROUP BY genre;
-- sqlite3.OperationalError: misuse of aggregate: COUNT()
```

When `WHERE` runs, there are no groups yet. Move the condition into `HAVING`. (The clause order is also wrong: `WHERE` must come before `GROUP BY`.)

**`= NULL` instead of `IS NULL`.** No error, just no rows. That's worse, because nothing tells you.

**Forgetting a tie-breaker.** `ORDER BY rating DESC` alone may return two 7.1-rated films in either order. Add `, title` when order matters.

**Misreading `near "...": syntax error`.** SQLite points at the word *where it got confused*, which is usually just after the real mistake. `near "FROM": syntax error` often means a trailing comma in the column list: `SELECT title, year, FROM films`.

**Integer division surprises.** `AVG` always gives a decimal, but `runtime / 60` doesn't. Write `60.0` when you want a decimal.

## Recap

- `SELECT columns FROM table` reads data; `AS` names a column.
- `WHERE` filters rows: `AND`, `OR`, `IN`, `BETWEEN`, `LIKE` (`%` = anything, `_` = one character).
- `NULL` means unknown: test it with `IS NULL`, never `= NULL`. Aggregates skip it.
- `ORDER BY ... DESC` sorts, with tie-breakers; `LIMIT` keeps the first N.
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` summarise rows; `GROUP BY` does it per group.
- `WHERE` filters rows before grouping; `HAVING` filters groups after.
