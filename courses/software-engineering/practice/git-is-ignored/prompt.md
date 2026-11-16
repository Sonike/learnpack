# A simplified `.gitignore` matcher

A `.gitignore` file lists patterns for files Git should never track: virtual environments, caches, secrets. Write a function that decides whether a path is ignored by a list of patterns, using a **simplified** version of Git's rules.

```python
def is_ignored(path: str, patterns: list[str]) -> bool:
```

- `path` is a file's path relative to the repo root, with `/` between folders, e.g. `"src/__pycache__/app.cpython-312.pyc"`.
- `patterns` are the lines of a `.gitignore` file.

Rules (simplified from real Git):
1. Skip blank lines and lines starting with `#` (comments).
2. A pattern starting with `!` is a **negation**: if it matches, the path is *not* ignored. Match the rest of the pattern (without the `!`) as usual.
3. Patterns are checked **in order** and the **last** one that matches decides. No match at all means "not ignored".
4. A pattern ending in `/` (like `build/`) matches **folders only**: the path is matched if any of its folders (every part except the last) matches the name.
5. Any other pattern that contains a `/` (like `docs/*.md` or `/config.ini`) is matched against the **whole path**. Remove a leading `/` first.
6. A pattern with no `/` (like `*.pyc` or `.env`) matches if **any part** of the path matches it, so `secrets` matches `secrets/key.txt` and `app/secrets`.

Match with `fnmatch.fnmatchcase(name, pattern)` from the standard library: `*` matches any characters and `?` matches one. (In real Git `*` never crosses a `/` and you can't un-ignore a file inside an ignored folder; we skip those details.)

## Example

```python
patterns = ["# Python", "__pycache__/", "*.pyc", ".env", "*.log", "!keep.log"]
is_ignored("app/__pycache__/app.cpython-312.pyc", patterns)  # True
is_ignored(".env", patterns)                                 # True
is_ignored("server.log", patterns)                           # True
is_ignored("keep.log", patterns)                             # False  (the later "!keep.log" wins)
is_ignored("app/main.py", patterns)                          # False
```
