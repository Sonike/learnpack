# Designing small systems

## Why this matters

So far you've designed functions and classes. Real features are bigger: a request comes in from a phone, touches an API, a database, maybe a background job and a cache, and something comes back. Before writing that code, someone has to decide which pieces exist and how they talk. As a junior you won't design a bank, but you will be asked "how would you build this?" in interviews and in planning meetings, and you'll read design documents every week. The skill is not knowing fancy technology. It's turning requirements into a few simple parts, and being honest about the trade-offs.

## From requirements to components

A **requirement** is something the system must do ("users can shorten a link") or a property it must have ("redirects must be fast", "we have one developer and no budget"). A **component** is one part of the system with a clear job. Most small web systems are built from the same five:

```
  +---------+      HTTP      +---------+      SQL      +------------+
  | Client  | -------------> |   API   | ------------> |  Database  |
  | browser |  <------------ | server  | <------------ |  (SQLite / |
  | or app  |    JSON        +---------+               |  Postgres) |
  +---------+                  |     ^                 +------------+
                               |     |
                   enqueue job |     | read / write
                               v     |
                        +------------+    +---------+
                        | Background |    |  Cache  |
                        |   worker   |    | (memory)|
                        +------------+    +---------+
```

- **Client:** what the user touches: a web page, a mobile app, another program. It never talks to the database directly.
- **API server:** your FastAPI app. It checks input, enforces the rules (who may do what), and talks to the other parts.
- **Database:** where data lives permanently. If the server restarts, the data survives.
- **Background job (worker):** work that is slow or can happen later, done outside the request: sending emails, resizing images, generating a monthly report. The API puts a job on a **queue** and answers the user immediately.
- **Cache:** a fast, temporary copy of data that is expensive to get, so you don't fetch or compute it again every time.

A useful habit is to go through the requirements one by one and ask which component owns each:

| Requirement | Component |
|---|---|
| Show a user their saved recipes | API reads from the database |
| A recipe must still exist tomorrow | Database |
| Email a weekly summary every Monday | Background job (on a schedule) |
| The home page is viewed 1,000 times a minute and changes hourly | Cache in front of the database |
| Only the owner can edit a recipe | API (authorisation check) |
| Works on phones | Client |

Notice that most rows land on the API and the database. For a junior-sized system that's normal and good. Every extra component is something else to deploy, monitor and debug.

## Trade-offs: there is no free choice

A **trade-off** is a choice where you gain one thing by giving up another. Design is mostly naming trade-offs out loud. Three you'll meet constantly:

**Simplicity vs scale.** One server with SQLite can handle far more traffic than most beginners expect: thousands of reads per second on modest hardware. A system with five services and a message queue can handle more, and is ten times harder to run. Start simple; add pieces when you can point at the problem they solve.

**SQLite vs Postgres.** SQLite is a file on the same machine: zero setup, great for one server, tests and small apps. Postgres is a separate database server: many app servers can share it, it handles lots of simultaneous writes, and hosted versions come with backups. A fair rule: SQLite while you have one server and modest writes; Postgres when you need several servers or many users writing at once. Because you used plain SQL and a repository layer, switching later is work, not a rewrite.

**Synchronous vs asynchronous (background) work.** Doing the work inside the request (synchronously) is simple: the user waits, then sees the result or the error. Pushing it to a background job keeps the request fast and lets you retry failures, but the user doesn't see the result immediately and you now have a queue and a worker to run. Rough rule: if it takes more than about a second, or it talks to a slow outside service, or it can be retried later, make it a job.

## Caching, and when it hurts

A cache stores answers so the next request is fast. Python even has one built in:

```python
from functools import lru_cache

calls = 0

@lru_cache(maxsize=128)
def exchange_rate(currency: str) -> float:
    global calls
    calls += 1                  # pretend this is a slow API call
    return {"EUR": 0.92, "GBP": 0.79}[currency]

exchange_rate("EUR"); exchange_rate("EUR"); exchange_rate("GBP")
print(calls)   # 2   (the second EUR came from the cache)
```

**LRU** stands for **least recently used**. A cache can't grow forever, so when it's full it throws away the entry that hasn't been used for the longest time, on the bet that recent things will be wanted again. `maxsize=128` is that limit, called the **capacity**.

Caches cause bugs, too. The famous one is **stale data**: the database changed, but the cache still serves the old value. Two common defences:

- a **TTL** (time to live): every entry expires after, say, 60 seconds, so stale data lives at most that long;
- **invalidation**: when you update the data, delete the cached copy at the same time.

So when should you add a cache? Only when all of these are true: something is measurably slow or expensive; the same thing is requested often; and showing slightly old data is acceptable. A user's bank balance fails the last test. A product catalogue page usually passes. If you can't name the slow thing you're fixing, don't add a cache yet.

In the practice exercises you'll build an LRU cache yourself, in O(1) time per operation, plus a TTL version that takes an injected clock so tests don't have to wait.

## The one-page design doc

Before building anything bigger than a day's work, teams write a short **design document**. One page is plenty at your level, with four parts:

```
# Design: Link shortener

## Problem
People share long URLs in SMS and printed flyers. We need short links
that redirect to the original.

## Constraints
- One developer, free hosting tier, ~1,000 new links/day, ~50,000 redirects/day.
- Short links must never collide or change once issued.

## Options
1. Random 7-character codes; check the database for collisions.
2. Database auto-increment ID encoded in base62.
3. Hash of the URL (first 7 characters of SHA-256).

## Decision
Option 2. IDs are unique by construction, so no collision checks.
Codes are short (62^6 ≈ 57 billion links in 6 characters).
Trade-off: codes are guessable in order. Acceptable: links aren't secret.
Revisit if we need private links (switch to option 1).
```

The most valuable line is usually the trade-off: it tells a future reader *why*, and when the decision should be reconsidered. Teams often keep each decision as a short **ADR** (architecture decision record) in the repository so the history survives.

## Interview-sized design: a URL shortener

Junior "system design" questions are at this level. Here's a calm way to answer, using the URL shortener:

1. **Clarify requirements.** Can users choose custom codes? Do links expire? Roughly how many links and clicks?
2. **Define the API.** `POST /links {"url": ...}` returns `{"code": "dnh"}`; `GET /{code}` responds with a `301` or `302` redirect to the original URL.
3. **Data model.** One table: `links(id INTEGER PRIMARY KEY, url TEXT NOT NULL, created_at TEXT)`.
4. **The key idea: generating codes.** Take the row's ID and write it in **base62**, using the 62 characters `0-9`, `a-z`, `A-Z`. This is the same as writing a number in base 10 or base 2, just with 62 digits:

   ```python
   ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

   def to_base62(n: int) -> str:
       if n == 0:
           return ALPHABET[0]
       digits = []
       while n > 0:
           n, remainder = divmod(n, 62)
           digits.append(ALPHABET[remainder])
       return "".join(reversed(digits))

   print(to_base62(61))      # Z
   print(to_base62(62))      # 10
   print(to_base62(125))     # 21
   ```

   Different IDs always give different codes, so collisions are impossible. Decoding goes the other way: `value = value * 62 + ALPHABET.index(char)` for each character.

5. **Scale, only if asked.** Redirects far outnumber new links, so the reads are the hot path: put a cache in front of `code → url` lookups. Since a code's URL never changes, there's no stale-data problem. That's a perfect cache.
6. **Name the trade-offs.** Sequential codes are guessable; a single database is a single point of failure; both are fine at this size.

Interviewers care more about steps 1, 5 and 6 (asking, reasoning, being honest) than about naming technologies.

## Technical debt

Every shortcut you take now (no tests for a module, a copy-pasted function, a hard-coded limit) is **technical debt**: like borrowing money, it buys speed today and charges interest later, as every future change in that area gets slower and riskier. Some debt is a sensible choice, for example shipping a prototype to learn whether anyone wants the feature. The problem is debt you don't know you took. Write it down (a `TODO` with a ticket, a line in the design doc's trade-offs) so the team can decide when to pay it back.

## Common mistakes

**Designing for a million users on day one.** Microservices, queues and Kubernetes for an app with ten users is the most common over-design. Choose the simplest thing that meets the stated requirements and explain how you'd grow it.

**Adding a cache without a reason.** It adds stale-data bugs and memory use. Measure first.

**Forgetting cache invalidation.** If the data can change, every write must update or delete the cached copy, or entries need a TTL.

**Base62 off-by-one bugs.** Forgetting the `n == 0` case returns an empty string; reversing the digits in the wrong place gives codes that decode to different numbers. Always test that `decode(encode(n)) == n` for many values, including 0.

**Skipping the "why".** A design doc that lists components but no trade-offs can't be reviewed. Write down what you gave up.

> **Try it:** In the practice editor, write `from_base62(code)` to reverse `to_base62`, then check `all(from_base62(to_base62(n)) == n for n in range(10_000))`.

## Recap

- Most small systems are a client, an API, a database, and sometimes a background job and a cache. Map each requirement to the component that owns it.
- Design is naming trade-offs: simplicity vs scale, SQLite vs Postgres, doing work now vs in a background job.
- Caches trade freshness for speed. LRU evicts the least recently used entry; TTLs and invalidation limit stale data. Add one only for something measured as slow, often requested, and fine to be slightly old.
- A one-page design doc covers problem, constraints, options and decision, including what you gave up.
- For interview design questions: clarify, define the API and data, solve the key problem simply, then discuss scale and trade-offs.
- Technical debt is fine when chosen and written down; dangerous when invisible.
