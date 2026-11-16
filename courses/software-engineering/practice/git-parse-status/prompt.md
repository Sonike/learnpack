# Read `git status --porcelain`

`git status` is written for people. `git status --porcelain` prints the same facts in a stable, machine-readable format that scripts and editors use. Each line looks like this:

```
XY path
```

- `X` (column 1) is the file's state in the **staging area**: what the next commit will contain.
- `Y` (column 2) is its state in the **working tree**: your files on disk, compared with the staging area.
- A space means "no change there". `M` = modified, `A` = added, `D` = deleted, `R` = renamed.
- `??` means the file is **untracked**: Git has never been told about it.
- The path starts at column 4 (index 3). For a rename the path looks like `old.py -> new.py`; use the new name.

Write a function that groups the paths:

```python
def parse_status_porcelain(text: str) -> dict[str, list[str]]:
```

- Return `{"staged": [...], "modified": [...], "untracked": [...]}`, every key present even when its list is empty, paths in the order they appear.
- **staged:** `X` is a letter (not a space and not `?`).
- **modified:** `Y` is a letter (not a space and not `?`). A file can be in both lists: `MM` means you staged a change and then edited the file again.
- **untracked:** the line starts with `??`.
- Skip blank lines and ignored files (`!!`).

## Example

```python
text = """M  app.py
 M README.md
MM utils.py
A  tests/test_app.py
R  old_name.py -> new_name.py
?? notes.txt
"""
parse_status_porcelain(text)
# {"staged": ["app.py", "utils.py", "tests/test_app.py", "new_name.py"],
#  "modified": ["README.md", "utils.py"],
#  "untracked": ["notes.txt"]}
```
