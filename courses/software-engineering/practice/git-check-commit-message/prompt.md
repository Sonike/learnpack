# Check a commit message

The widely used "seven rules of a great Git commit message" (from Chris Beams' article, linked in the lesson) are easy to check with code. Write a checker that a team could run as a Git hook.

```python
def check_commit_message(msg: str) -> list[str]:
```

`msg` is the full commit message: a **subject** line, then optionally a blank line and a **body**. Before checking anything:
- Remove every line that starts with `#` (Git treats those as comments and drops them too).
- Remove trailing blank lines.

If nothing is left, return `["Message is empty"]` and stop. Otherwise return every problem below that applies, in this order (an empty list means the message is good):

| Rule | Problem text |
|---|---|
| Subject is at most 50 characters | `"Subject is 62 characters (keep it to 50)"` with the real length |
| Subject starts with a capital letter | `"Capitalize the subject line"` (only when the first character is a lowercase letter) |
| Subject doesn't end with a period | `"Do not end the subject with a period"` |
| Subject uses the imperative mood | `'Use the imperative mood ("Fix bug", not "Fixed bug")'` |
| Line 2, if there is one, is blank | `"Separate subject from body with a blank line"` |
| Body lines are at most 72 characters | `"Body line 4 is 80 characters (wrap at 72)"`, one per long line, numbered from 1 = the subject |

**Imperative mood** can't be checked perfectly without a dictionary, so use this heuristic: take the subject's first word in lowercase; it's **not** imperative if it ends in `"ed"` or `"ing"` (like `Added`, `Fixing`), unless it's one of the words in `IMPERATIVE_EXCEPTIONS` (like `embed`, `bring`). A real tool would use a word list; heuristics with exceptions are common in linters.

## Example

```python
check_commit_message("Add password reset email\n\nUsers had to email support to get back in.")
# []

check_commit_message("fixed the login bug that happened when the password was empty.")
# ["Subject is 62 characters (keep it to 50)", "Capitalize the subject line",
#  "Do not end the subject with a period", 'Use the imperative mood ("Fix bug", not "Fixed bug")']
```
