# Reading code and open source

## Why this matters

As a working engineer you'll read far more code than you write. Your first tickets will be in a codebase of tens or hundreds of thousands of lines that other people wrote over years. Nobody expects you to understand all of it. They do expect you to find your way to the part that matters, quickly and without breaking things. Open source projects are the best free place to practise that skill, and a merged contribution is strong evidence on a resume.

## You don't read a codebase like a book

The instinct is to open the first file and read top to bottom. That doesn't work: the order of files on disk has nothing to do with the order the program runs. Instead, read with a **question** in mind ("how does a search request get answered?") and follow the code that answers it.

Here's a route that works on almost any project:

```
 1. README          What is it? How do I install and run it?
 2. Run it          Get it working locally. Click around or call it.
 3. Run the tests   Proves your setup works; shows what "correct" means.
 4. Entry point     Where does execution start?
 5. Follow one path Trace one request or command end to end.
 6. Read tests      Tests are examples of how each piece is meant to be used.
```

### 1. The README

A good README answers: what is this, how do I install it, how do I run it, how do I run the tests. Also look for `CONTRIBUTING.md` (how the maintainers want you to work), `LICENSE` (what you're allowed to do with the code) and a `docs/` folder.

### 2 and 3. Run it, then run the tests

Before changing anything, make it work as-is:

```bash
git clone https://github.com/example/booktracker.git
cd booktracker
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
# ======================== 142 passed in 3.21s ========================
```

If the tests pass, you have a safety net: when one fails later, it's because of *your* change. If they don't pass on a fresh clone, you've found something worth asking about (or fixing in the README).

### 4. Find the entry point

Every program starts somewhere. In Python projects, look for:

- `if __name__ == "__main__":` in a file, often `main.py` or `cli.py`
- `[project.scripts]` in `pyproject.toml`, which names the function a command runs
- `app = FastAPI()` (or `Flask(__name__)`) for web services
- `__main__.py` inside a package, which runs for `python -m package`

### 5. Follow one path

Pick one concrete action, such as "GET /books?title=dune", and trace it: the route function, what it calls, what that calls, down to the database query and back. Write the chain down as you go:

```
GET /books?title=dune
  └─ routes/books.py: list_books(title)
       └─ services/catalog.py: search(title)
            └─ repo/books.py: find_by_title(conn, title)  ← the SQL lives here
```

After one path, the rest of the codebase starts to make sense, because most paths look alike.

## Tools for moving around

You don't need to read every file to find what you need. Two tools do most of the work.

**Search with `grep`** (or your editor's "Find in files"). Looking for where an error message comes from? Search for the exact text:

```bash
grep -rn "Book not found" --include="*.py" .
# ./booktracker/routes/books.py:48:        raise HTTPException(404, "Book not found")
```

`-r` searches folders recursively, `-n` shows line numbers, and `--include` limits it to Python files. Searching for a distinctive error message is often the fastest way into unfamiliar code.

**Go to definition and find references.** In VS Code, hold Cmd (Mac) or Ctrl (Windows/Linux) and click a function name to jump to where it's defined. Right-click → "Find All References" shows everywhere it's used. Use these constantly.

## Seeing structure: the call graph

A **call graph** shows which functions call which. Editors build one internally to power "find references". You can build a simple version yourself with Python's `ast` module.

`ast` stands for **abstract syntax tree**. `ast.parse` turns source code into a tree of objects, one per piece of syntax, that you can inspect without running the code:

```python
import ast

tree = ast.parse("total = add(price, tax)")
print(ast.dump(tree.body[0].value))
# Call(func=Name(id='add'), args=[Name(id='price'), Name(id='tax')])
```

(Python 3.12 prints a longer version with extra `ctx=Load()` details; the structure is the same.)

The call `add(price, tax)` became a `Call` node whose `func` is a `Name` with `id='add'`. `ast.walk(node)` visits every node inside another node, so finding every call inside a function is a short loop:

```python
import ast

source = """
def load(path):
    return open(path).read()

def main(path):
    print(load(path))
"""
tree = ast.parse(source)
for func in tree.body:
    calls = [n.func.id for n in ast.walk(func)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    print(func.name, calls)
# load ['open']
# main ['print', 'load']
```

In the exercise you'll turn this into `call_graph`, keeping only calls to functions defined in the same module. Tools like linters, formatters and the "go to definition" feature in your editor are built on exactly this kind of tree.

## Contributing to open source

**Open source** software is code published under a license that lets anyone read, use, modify and share it. Python itself, pytest, FastAPI and Git are all open source. Most of them welcome new contributors.

### Finding a first issue

- Look for issues labelled **good first issue** or **help wanted** on GitHub. You can search across GitHub for `label:"good first issue" language:Python`.
- Start with projects **you already use**. You know what they're for, and you may have hit a bug or a confusing doc already.
- **Documentation fixes count.** A clearer README, a fixed example or a typo fix is a real contribution, and a gentle way to learn a project's process.

### Etiquette

- **Read `CONTRIBUTING.md` first.** It tells you how to set up, the code style, how to run tests, and whether they want an issue before a PR.
- **Comment before you start.** "I'd like to work on this; my plan is X. Does that sound right?" Avoids two people fixing the same thing, and avoids building something the maintainers don't want.
- **Keep the PR small and focused.** One fix per PR. Don't reformat files you didn't otherwise change.
- **Follow the template**, link the issue ("Fixes #123"), and say how you tested it.
- **Be patient and polite.** Maintainers are often volunteers. A week without a reply is normal; a friendly nudge after that is fine.
- **Accept "no" gracefully.** Sometimes a PR doesn't fit the project's direction. You still learned the codebase.

### Licenses

A **license** is the legal permission to use code. Code on GitHub with *no* license is, by default, not free to reuse. Common open source licenses:

```
 MIT, BSD, Apache 2.0   "Permissive": use it anywhere, even in closed
                        products, keep the copyright notice.
 GPL                    "Copyleft": if you distribute software that includes
                        it, you must release your code under the GPL too.
```

For your own portfolio projects, MIT is a common, simple choice. choosealicense.com explains the options in plain language. At work, never copy code from the internet into the company codebase without checking its license, and follow your company's policy.

## Common mistakes

- **Reading every file before doing anything.** Read with a question, follow one path.
- **Changing code before running the tests.** If something then fails, you can't tell whether you broke it or it was already broken.
- **Opening a large PR to a project without talking to the maintainers.** Comment on the issue first.
- **"Cleaning up" unrelated code in a fix.** Reviewers then have to check every change. Keep it focused.
- **Ignoring `CONTRIBUTING.md`.** Your PR gets bounced for missing a changelog entry or a signed commit.
- **Assuming code without a license is free to use.** It isn't.

## Recap

- Read code with a question. Route: README → run it → run the tests → entry point → follow one path → read the tests.
- Use `grep -rn` for exact text (error messages are great entry points) and "go to definition" / "find references" in your editor.
- `ast.parse` turns source into a tree you can inspect; calls are `ast.Call` nodes. Tools you use daily are built on this.
- For open source: start with projects you use, look for "good first issue", read `CONTRIBUTING.md`, comment before starting, keep PRs small.
- Licenses decide what you may do with code: permissive (MIT, Apache) vs copyleft (GPL). No license means no permission.
