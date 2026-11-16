# Lint a pull request description

Reviewers move faster when every pull request (PR) description answers the same three questions and links the issue it solves. Many teams check this automatically. Write the check.

```python
def lint_pr_description(md: str) -> list[str]:
```

- `md` is the PR description, written in Markdown.
- Return a list of problems, in this order (an empty list means the description is fine):
  1. For each of the sections **What**, **Why** and **How to test**, in that order, if there's no heading for it: `"Missing section: What"` (or `Why`, `How to test`). A heading is a line made of 1 to 6 `#` characters, a space, and the section name. Ignore case and a trailing colon: `## how to test:` counts.
  2. If there's no issue reference like `#123` anywhere (a `#` followed straight away by digits): `"No linked issue (add e.g. Closes #123)"`.
  3. If a line starts with `Size:` (any case) followed by a number of changed lines, and that number is over 400: `"Too big: 520 changed lines (aim for under 400)"` with the real number. No `Size:` line means no size problem.

## Example

```python
good = """## What
Add a password reset email.

## Why
Users locked out of their accounts had to email support. Closes #42.

## How to test
1. Run `pytest tests/test_reset.py`
2. Request a reset for a test account and open the link.

Size: 180 lines
"""
lint_pr_description(good)   # []

lint_pr_description("Fixed stuff\n\nSize: 950")
# ["Missing section: What", "Missing section: Why", "Missing section: How to test",
#  "No linked issue (add e.g. Closes #123)", "Too big: 950 changed lines (aim for under 400)"]
```

Hint: the `re` module helps. `re.search(r"#\d+", md)` finds an issue reference; `re.MULTILINE` lets `^` match at the start of every line.
