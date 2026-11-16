# Code review

## Why this matters

On almost every professional team, no code reaches `main` until another engineer has read it. That's **code review**, and as a junior you'll spend hours a week on both sides of it: getting your pull requests reviewed and reviewing other people's. Review catches bugs, but it also spreads knowledge, keeps the codebase consistent, and is where you learn fastest. How you write and receive review comments is also one of the clearest signals of whether you're good to work with.

## What a review is

You already know the mechanics from the Git and GitHub section: you push a branch, open a **pull request** (PR), and teammates comment on specific lines. Some companies call a PR a **merge request** (GitLab) or a **CL**, short for "changelist" (Google). They all mean a proposed change waiting for review.

A review ends in one of three states:

- **Approve**: good to merge, maybe with small optional comments.
- **Comment**: questions or suggestions, no decision yet.
- **Request changes**: something must be fixed before merging.

Google's guidelines, used by thousands of engineers and free to read, give the standard to aim for: approve a change once it **definitely improves the overall health of the code**, even if it isn't perfect. Review is not about making the code exactly how *you* would write it.

## What reviewers look for

Reviewers work roughly from the most important thing to the least:

```
 1. Design         Does this change belong here? Is the approach sound?
 2. Functionality  Does it do what the ticket says? Edge cases? Security?
 3. Complexity     Could it be simpler? Will the next person understand it?
 4. Tests          Are there tests? Would they fail if the code broke?
 5. Naming         Do names say what things are and do?
 6. Comments       Do comments explain *why*, not repeat *what*?
 7. Style          Consistent with the codebase? (Let the linter do this.)
```

Here's a small change to review. Read it before you read on.

```python
def find(db, q):
    sql = f"SELECT id, title FROM books WHERE title LIKE '%{q}%'"
    try:
        rows = db.execute(sql).fetchall()
    except Exception:
        rows = []
    return rows[:25]
```

It runs, and for normal searches it returns the right books. A careful reviewer would still find five problems:

1. **SQL injection** (functionality, security). `q` comes from the user and goes straight into the SQL text. A search for `' OR 1=1 --` changes the query. This blocks the merge.
2. **A swallowed exception** (functionality). If the database is down, `except Exception: rows = []` turns the outage into "no results found", and nobody ever learns about it.
3. **No tests.** Nothing proves the search works, or that the injection is fixed.
4. **Unclear names.** `find` finds what? `q` is what?
5. **A magic number.** Why 25? A named constant like `MAX_RESULTS = 25` explains it.

Here's the version that would pass review:

```python
MAX_RESULTS = 25


def search_books_by_title(db, text):
    sql = "SELECT id, title FROM books WHERE title LIKE ? LIMIT ?"
    return db.execute(sql, (f"%{text}%", MAX_RESULTS)).fetchall()
```

The `?` placeholders send the user's text as data, never as SQL. If the database fails, the error propagates to code that can log it and return a proper error. And `LIMIT` lets the database do the cutting.

## Writing good review comments

A comment has to do two jobs: be **specific** enough to act on, and **kind** enough that the author wants to act on it. Compare:

```
Bad:   This is wrong.
Bad:   Why would you ever loop like this??
Good:  This loops over every order for each user, so it's O(n·m).
       A dict from user_id to orders would make it O(n + m).
       Happy to pair on it if useful.
```

The good one says **what** the problem is, **why** it matters, and **suggests** a fix. It talks about the code ("this loops"), not the person ("you always…").

A few habits that make comments better:

- **Ask when you're not sure.** "Is there a reason this isn't using the existing `parse_date` helper?" There might be a reason you don't know.
- **Explain why.** "Please add a test" is weaker than "Please add a test for the empty-list case; that's the one that crashed in production last month."
- **Praise good things.** "Nice, this test name explains the bug exactly." Review isn't only for problems, and it tells the author what to keep doing.
- **Suggest, don't dictate, on matters of taste.** If both ways are fine, it's not worth a comment, or it's a nit.

## Labelling comments: blocking, nit, question, praise

The author needs to know which comments **must** be addressed before merging. Many teams use **conventional prefixes**:

```
issue: this builds SQL from user input, so it's open to injection.
nit: a MAX_RESULTS constant would explain the 25.
question: why a list here and not a set?
praise: great test names.
```

- **Blocking** (`issue:`, `blocking:`) must be fixed before merge.
- **Nit** (`nit:`, short for nitpick) is a small, optional polish. The author can ignore it.
- **Question** asks for understanding. Sometimes the answer leads to a change, sometimes to a code comment explaining the reason.
- **Praise** is exactly what it sounds like.

Google's guide notes that a comment *without* a label is usually read as something the author should address. So if a comment is optional, say so.

Here's a tiny version of the classifier you'll write in this lesson's exercise:

```python
def label_of(comment):
    prefix = comment.split(":", 1)[0].strip().lower()
    return prefix if prefix in {"nit", "question", "praise", "issue"} else None

print(label_of("nit: extra blank line"))     # nit
print(label_of("This leaks the token"))      # None
```

## Being a good author

Most of the review experience is decided before the reviewer opens your PR.

**Review your own diff first.** Before requesting review, read every changed line in GitHub's "Files changed" tab as if you were the reviewer. You'll catch leftover `print` calls, commented-out code and typos, and save a round trip.

**Keep PRs small.** Google's guide recommends small changes because they're reviewed faster, more thoroughly, and are less likely to hide bugs. A PR under about 200 lines usually gets a careful review within hours. A 2,000-line PR gets either "LGTM" (looks good to me) without real reading, or a week of delay. If your feature is big, ship it in pieces.

**Describe the why.** The PR description should let a reviewer understand the change without asking you:

```
## What
Adds search by title to the /books endpoint.

## Why
Members asked for it in #112; browsing 3,000 books is slow.

## How
Parameterised LIKE query with a limit of 25. Considered full-text search
(FTS5) but it's overkill at this size; noted in the design doc.

## Testing
New tests for: match, no match, special characters, injection attempt.
```

**Respond to every comment.** Either make the change and reply "Done", or explain why not. Don't silently ignore comments, and don't resolve someone else's comment thread without replying.

## Handling disagreement

Sometimes you'll disagree with a reviewer, or they with you. Some ground rules:

- **Assume good intent.** Text loses tone. "Why did you do it this way?" is usually curiosity, not an attack.
- **Argue with evidence.** Data, docs, a style guide, or a quick benchmark beat "I prefer".
- **Take it off the page.** After two rounds of back-and-forth, talk it through on a call. It's faster and friendlier. Then write the outcome back in the PR so it's recorded.
- **Know who decides.** On matters of taste, the author usually wins. On correctness, security and team standards, the standard wins. If you're truly stuck, ask the tech lead.
- **You're not your code.** A comment on your code isn't a comment on you. The best engineers you'll work with get the most review comments, because they ask for them.

## Reviewing AI-generated code

More and more PRs contain code written with an AI assistant. Review it with **extra** care, not less. AI-written code tends to look clean and confident, which makes problems easy to miss. Common issues include:

- functions or library options that don't exist
- broad `try`/`except` blocks that hide failures
- edge cases quietly skipped (empty input, time zones, off-by-one)
- tests that check the code does what it does, rather than what it *should* do

The author is responsible for every line, whoever typed it. As a reviewer, it's fair to ask "Can you walk me through this part?" If the author can't explain it, it isn't ready. You'll practise this directly in the lesson "Using AI tools responsibly".

## Common mistakes

- **Rubber-stamping.** Approving with "LGTM" without reading. If you don't have time to review properly, say so and let someone else take it.
- **Reviewing style by hand.** Arguing about spaces and quotes wastes everyone's time. A formatter like ruff settles it automatically.
- **Unlabelled nits.** If ten small comments look equally urgent, the author can't tell what matters. Label them.
- **Huge PRs.** They get worse reviews. Split them.
- **Taking comments personally**, or writing comments that are personal. Keep it about the code.
- **Leaving review for days.** Teams usually aim to respond to a review request within one working day. A waiting PR blocks a teammate.

## Recap

- Code review is how teams keep quality and share knowledge. Approve when a change **improves the code's health**, even if it isn't perfect.
- Reviewers look at design, functionality (including security), complexity, tests, naming and comments, in roughly that order.
- Good comments are specific (what, why, suggestion) and kind (about the code, not the person). Praise counts too.
- Label comments: `issue:`/blocking, `nit:`, `question:`, `praise:`. Unlabelled usually means "please address".
- As an author: self-review, keep PRs small, describe the why, and reply to every comment.
- Disagree with evidence, move long threads to a call, and record the outcome.
- Review AI-written code with extra care; the author owns every line.
